"""
Stage 03 - Segmentation
U-Net model that segments the person's body/clothing region from the
background. The resulting mask is used by 05_body_analysis.py and
06_garment_processing.py.

Usage:
    python 03_segmentation.py   # trains a quick U-Net on the dataset
"""

import importlib

import torch
import torch.nn as nn

import config

preprocessing = importlib.import_module("02_data_preprocessing")


class DoubleConv(nn.Module):
    def __init__(self, in_ch, out_ch):
        super().__init__()
        self.net = nn.Sequential(
            nn.Conv2d(in_ch, out_ch, 3, padding=1),
            nn.BatchNorm2d(out_ch),
            nn.ReLU(inplace=True),
            nn.Conv2d(out_ch, out_ch, 3, padding=1),
            nn.BatchNorm2d(out_ch),
            nn.ReLU(inplace=True),
        )

    def forward(self, x):
        return self.net(x)


class UNet(nn.Module):
    def __init__(self, in_ch=3, out_ch=1, base=64):
        super().__init__()
        self.down1 = DoubleConv(in_ch, base)
        self.down2 = DoubleConv(base, base * 2)
        self.down3 = DoubleConv(base * 2, base * 4)
        self.down4 = DoubleConv(base * 4, base * 8)
        self.pool = nn.MaxPool2d(2)

        self.bottleneck = DoubleConv(base * 8, base * 16)

        self.up4 = nn.ConvTranspose2d(base * 16, base * 8, 2, stride=2)
        self.upconv4 = DoubleConv(base * 16, base * 8)
        self.up3 = nn.ConvTranspose2d(base * 8, base * 4, 2, stride=2)
        self.upconv3 = DoubleConv(base * 8, base * 4)
        self.up2 = nn.ConvTranspose2d(base * 4, base * 2, 2, stride=2)
        self.upconv2 = DoubleConv(base * 4, base * 2)
        self.up1 = nn.ConvTranspose2d(base * 2, base, 2, stride=2)
        self.upconv1 = DoubleConv(base * 2, base)

        self.out_conv = nn.Conv2d(base, out_ch, 1)

    def forward(self, x):
        d1 = self.down1(x)
        d2 = self.down2(self.pool(d1))
        d3 = self.down3(self.pool(d2))
        d4 = self.down4(self.pool(d3))

        b = self.bottleneck(self.pool(d4))

        u4 = self.up4(b)
        u4 = self.upconv4(torch.cat([u4, d4], dim=1))
        u3 = self.up3(u4)
        u3 = self.upconv3(torch.cat([u3, d3], dim=1))
        u2 = self.up2(u3)
        u2 = self.upconv2(torch.cat([u2, d2], dim=1))
        u1 = self.up1(u2)
        u1 = self.upconv1(torch.cat([u1, d1], dim=1))

        return torch.sigmoid(self.out_conv(u1))


def train_segmentation(model, loader, epochs=config.SEGMENTATION_EPOCHS,
                        lr=config.SEGMENTATION_LR, device=config.DEVICE):
    model = model.to(device)
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)
    criterion = nn.BCELoss()

    for epoch in range(epochs):
        model.train()
        total_loss, n = 0.0, 0

        for batch in loader:
            if "mask" not in batch:
                raise KeyError(
                    "Batch has no 'mask' key. Make sure config.MASK_DIR "
                    "points to a valid folder with segmentation masks."
                )

            imgs = batch["person"].to(device)
            masks = batch["mask"].to(device)

            optimizer.zero_grad()
            pred = model(imgs)
            loss = criterion(pred, masks)
            loss.backward()
            optimizer.step()

            total_loss += loss.item() * imgs.size(0)
            n += imgs.size(0)

        print(f"[segmentation] epoch {epoch + 1}/{epochs} | loss: {total_loss / n:.4f}")

    return model


def load_segmentation_model(checkpoint_path, device=config.DEVICE):
    model = UNet().to(device)
    model.load_state_dict(torch.load(checkpoint_path, map_location=device))
    model.eval()
    return model


if __name__ == "__main__":
    dataset = preprocessing.VTONDataset()
    loader = preprocessing.get_dataloader(dataset)

    model = UNet()
    trained = train_segmentation(model, loader)

    ckpt_path = f"{config.CHECKPOINT_DIR}/segmentation.pth"
    torch.save(trained.state_dict(), ckpt_path)
    print(f"Saved segmentation model to {ckpt_path}")
