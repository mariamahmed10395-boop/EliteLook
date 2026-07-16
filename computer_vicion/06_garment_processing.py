"""
Stage 06 - Garment Processing
Two responsibilities:
  1. GarmentClassifier - classifies garment type (t-shirt, pants, dress, ...).
     If the dataset has no explicit labels, KMeans clustering produces
     pseudo-labels as a fallback.
  2. GarmentWarper - warps the cloth image (TPS-style) so it aligns with the
     target person's body shape/pose, ready to be merged in 07_virtual_tryon.py.

Usage:
    python 06_garment_processing.py
"""

import importlib

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from PIL import Image
from sklearn.cluster import KMeans

import config

preprocessing = importlib.import_module("02_data_preprocessing")


# ---------------------------------------------------------------------------
# 1. Garment classification
# ---------------------------------------------------------------------------
class GarmentClassifier(nn.Module):
    def __init__(self, num_classes=config.NUM_GARMENT_CLASSES):
        super().__init__()
        self.features = nn.Sequential(
            nn.Conv2d(3, 32, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
            nn.Conv2d(32, 64, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
            nn.Conv2d(64, 128, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
            nn.Conv2d(128, 256, 3, padding=1), nn.ReLU(), nn.AdaptiveAvgPool2d(1),
        )
        self.classifier = nn.Linear(256, num_classes)

    def forward(self, x):
        x = self.features(x)
        x = x.view(x.size(0), -1)
        return self.classifier(x)


def train_classifier(model, loader, epochs=config.CLASSIFIER_EPOCHS,
                      lr=config.CLASSIFIER_LR, device=config.DEVICE):
    """loader must yield (image, label) pairs, e.g. from torchvision.datasets.ImageFolder."""
    model = model.to(device)
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)
    criterion = nn.CrossEntropyLoss()

    for epoch in range(epochs):
        model.train()
        total_loss, correct, total = 0.0, 0, 0

        for imgs, labels in loader:
            imgs, labels = imgs.to(device), labels.to(device)
            optimizer.zero_grad()
            out = model(imgs)
            loss = criterion(out, labels)
            loss.backward()
            optimizer.step()

            total_loss += loss.item() * imgs.size(0)
            correct += (out.argmax(1) == labels).sum().item()
            total += imgs.size(0)

        print(f"[classifier] epoch {epoch + 1}/{epochs} | "
              f"loss: {total_loss / total:.4f} | acc: {correct / total:.4f}")

    return model


def cluster_garments(cloth_paths, n_clusters=config.NUM_GARMENT_CLASSES):
    """
    Fallback for datasets without explicit garment-type labels: extracts a
    cheap flattened-pixel feature and clusters it with KMeans to produce
    pseudo-labels.
    """
    feats = []
    for p in cloth_paths:
        img = Image.open(p).convert("RGB").resize((32, 32))
        feats.append(np.array(img).flatten() / 255.0)
    feats = np.stack(feats)

    km = KMeans(n_clusters=n_clusters, random_state=config.SEED, n_init=10)
    pseudo_labels = km.fit_predict(feats)
    return pseudo_labels, km


# ---------------------------------------------------------------------------
# 2. Garment warping (TPS)
# ---------------------------------------------------------------------------
class TPSGridGen(nn.Module):
    """
    Generates a sampling grid from predicted control points for use with
    F.grid_sample. This is a simplified bilinear-grid version; swap in a
    full closed-form TPS solver for production-quality warping.
    """

    def __init__(self, out_h, out_w, grid_size=config.TPS_GRID_SIZE):
        super().__init__()
        self.out_h, self.out_w = out_h, out_w
        self.grid_size = grid_size

    def forward(self, source_control_points):
        batch_size = source_control_points.size(0)
        device = source_control_points.device

        yy, xx = torch.meshgrid(
            torch.linspace(-1, 1, self.out_h, device=device),
            torch.linspace(-1, 1, self.out_w, device=device),
            indexing="ij",
        )
        grid = torch.stack([xx, yy], dim=-1).unsqueeze(0).repeat(batch_size, 1, 1, 1)
        return grid


class GarmentWarper(nn.Module):
    """Predicts TPS control points and warps the cloth image accordingly."""

    def __init__(self, grid_size=config.TPS_GRID_SIZE, img_size=config.IMG_SIZE):
        super().__init__()
        self.grid_size = grid_size
        n_points = grid_size * grid_size

        self.encoder = nn.Sequential(
            nn.Conv2d(6, 32, 4, 2, 1), nn.ReLU(),
            nn.Conv2d(32, 64, 4, 2, 1), nn.ReLU(),
            nn.Conv2d(64, 128, 4, 2, 1), nn.ReLU(),
            nn.Conv2d(128, 256, 4, 2, 1), nn.ReLU(),
            nn.AdaptiveAvgPool2d(1),
        )
        self.regressor = nn.Linear(256, n_points * 2)
        self.tps = TPSGridGen(img_size, img_size, grid_size)

    def forward(self, person_repr, cloth):
        x = torch.cat([person_repr, cloth], dim=1)
        feat = self.encoder(x).view(x.size(0), -1)
        control_points = torch.tanh(self.regressor(feat)).view(-1, self.grid_size ** 2, 2)

        grid = self.tps(control_points)
        warped_cloth = F.grid_sample(cloth, grid, align_corners=True)

        return warped_cloth, control_points


def train_warper(model, loader, epochs=config.GARMENT_WARP_EPOCHS,
                  lr=config.GARMENT_WARP_LR, device=config.DEVICE):
    """
    Self-supervised training: the warped cloth is pushed towards the person
    image. Prefer using person * mask as the target if masks are available,
    since it isolates the actual garment region.
    """
    model = model.to(device)
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)
    criterion = nn.L1Loss()

    for epoch in range(epochs):
        model.train()
        total_loss, n = 0.0, 0

        for batch in loader:
            person = batch["person"].to(device)
            cloth = batch["cloth"].to(device)

            if "mask" in batch:
                target_region = person * batch["mask"].to(device)
            else:
                target_region = person

            optimizer.zero_grad()
            warped, _ = model(person, cloth)
            loss = criterion(warped, target_region)
            loss.backward()
            optimizer.step()

            total_loss += loss.item() * person.size(0)
            n += person.size(0)

        print(f"[warper] epoch {epoch + 1}/{epochs} | loss: {total_loss / n:.4f}")

    return model


if __name__ == "__main__":
    dataset = preprocessing.VTONDataset()
    loader = preprocessing.get_dataloader(dataset)

    # --- garment warping demo ---
    warper = GarmentWarper()
    trained_warper = train_warper(warper, loader)
    torch.save(trained_warper.state_dict(), f"{config.CHECKPOINT_DIR}/garment_warper.pth")
    print("Saved garment warper checkpoint.")

    # --- clustering fallback demo (no labels needed) ---
    pseudo_labels, _ = cluster_garments(dataset.cloth_paths)
    print("Pseudo-label distribution:", np.bincount(pseudo_labels))
