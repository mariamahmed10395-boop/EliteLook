"""
Stage 07 - Virtual Try-On
Generator (U-Net) + PatchGAN discriminator that synthesize the final
try-on image from (person, warped cloth). Also defines the end-to-end
VirtualTryOnPipeline combining 06_garment_processing's warper with this
generator, which is what 08_model_training.py trains.

Usage:
    python 07_virtual_tryon.py
"""

import importlib

import torch
import torch.nn as nn

import config

preprocessing = importlib.import_module("02_data_preprocessing")
segmentation = importlib.import_module("03_segmentation")
garment_processing = importlib.import_module("06_garment_processing")

UNet = segmentation.UNet
GarmentWarper = garment_processing.GarmentWarper


class Pix2PixGenerator(nn.Module):
    """U-Net generator with 6 input channels (person + cloth concatenated)."""

    def __init__(self, in_ch=6, out_ch=3, base=64):
        super().__init__()
        self.net = UNet(in_ch=in_ch, out_ch=out_ch, base=base)

    def forward(self, person, cloth):
        x = torch.cat([person, cloth], dim=1)
        out = self.net(x)
        return torch.tanh(out)  # output in [-1, 1]


class PatchDiscriminator(nn.Module):
    """70x70 PatchGAN discriminator, conditioned on (person, cloth, image)."""

    def __init__(self, in_ch=9):
        super().__init__()
        self.model = nn.Sequential(
            nn.Conv2d(in_ch, 64, 4, 2, 1), nn.LeakyReLU(0.2, inplace=True),
            nn.Conv2d(64, 128, 4, 2, 1), nn.BatchNorm2d(128), nn.LeakyReLU(0.2, inplace=True),
            nn.Conv2d(128, 256, 4, 2, 1), nn.BatchNorm2d(256), nn.LeakyReLU(0.2, inplace=True),
            nn.Conv2d(256, 512, 4, 1, 1), nn.BatchNorm2d(512), nn.LeakyReLU(0.2, inplace=True),
            nn.Conv2d(512, 1, 4, 1, 1),
        )

    def forward(self, person, cloth, img):
        x = torch.cat([person, cloth, img], dim=1)
        return self.model(x)


class VirtualTryOnPipeline(nn.Module):
    """
    Full two-stage pipeline:
      1. GarmentWarper aligns the cloth image to the person's body/pose.
      2. Pix2PixGenerator merges the person image with the warped cloth
         into the final try-on result.
    """

    def __init__(self, grid_size=config.TPS_GRID_SIZE):
        super().__init__()
        self.warper = GarmentWarper(grid_size=grid_size)
        self.generator = Pix2PixGenerator(in_ch=6, out_ch=3)

    def forward(self, person, cloth):
        warped_cloth, control_points = self.warper(person, cloth)
        result = self.generator(person, warped_cloth)
        return result, warped_cloth, control_points


def quick_forward_check(device=config.DEVICE):
    """Sanity check: run one batch through the full pipeline + discriminator."""
    dataset = preprocessing.VTONDataset()
    loader = preprocessing.get_dataloader(dataset, batch_size=2)
    batch = next(iter(loader))

    person = batch["person"].to(device)
    cloth = batch["cloth"].to(device)

    pipeline = VirtualTryOnPipeline().to(device)
    discriminator = PatchDiscriminator().to(device)

    result, warped_cloth, control_points = pipeline(person, cloth)
    pred = discriminator(person, cloth, result)

    print("result shape        :", result.shape)
    print("warped_cloth shape  :", warped_cloth.shape)
    print("control_points shape:", control_points.shape)
    print("discriminator output:", pred.shape)


if __name__ == "__main__":
    quick_forward_check()
