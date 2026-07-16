"""
Stage 04 - Pose Estimation
Extracts body keypoints (OpenPose-style, 18 points) from person images using
MediaPipe, and defines a lightweight CNN that can be trained to regress those
keypoints directly (useful once you no longer want to depend on MediaPipe at
inference time). Output keypoints feed into 05_body_analysis.py and
06_garment_processing.py.

Usage:
    python 04_pose_estimation.py
"""

import importlib

import numpy as np
import torch
import torch.nn as nn
import cv2

import config

preprocessing = importlib.import_module("02_data_preprocessing")

try:
    import mediapipe as mp
    _mp_pose = mp.solutions.pose
except ImportError:
    _mp_pose = None


def extract_keypoints_mediapipe(image_path, n_points=config.NUM_KEYPOINTS):
    """
    Returns an (n_points, 2) array of pixel coordinates for the detected
    body landmarks, or None if no person was detected.
    """
    if _mp_pose is None:
        raise ImportError("mediapipe is not installed. Run: pip install mediapipe")

    img = cv2.imread(image_path)
    if img is None:
        return None

    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    with _mp_pose.Pose(static_image_mode=True) as pose:
        result = pose.process(img_rgb)

    if not result.pose_landmarks:
        return None

    h, w = img.shape[:2]
    keypoints = []
    for lm in result.pose_landmarks.landmark[:n_points]:
        keypoints.append([lm.x * w, lm.y * h])

    return np.array(keypoints, dtype=np.float32)


class PoseEstimator(nn.Module):
    """CNN that regresses (x, y) coordinates for n_keypoints directly from an image."""

    def __init__(self, n_keypoints=config.NUM_KEYPOINTS):
        super().__init__()
        self.n_keypoints = n_keypoints
        self.backbone = nn.Sequential(
            nn.Conv2d(3, 32, 4, 2, 1), nn.ReLU(),    # H/2
            nn.Conv2d(32, 64, 4, 2, 1), nn.ReLU(),   # H/4
            nn.Conv2d(64, 128, 4, 2, 1), nn.ReLU(),  # H/8
            nn.Conv2d(128, 256, 4, 2, 1), nn.ReLU(), # H/16
            nn.AdaptiveAvgPool2d(1),
        )
        self.head = nn.Linear(256, n_keypoints * 2)

    def forward(self, x):
        feat = self.backbone(x).view(x.size(0), -1)
        out = self.head(feat)
        return out.view(-1, self.n_keypoints, 2)


class PoseDataset(torch.utils.data.Dataset):
    """
    Wraps VTONDataset and generates keypoint targets on the fly via MediaPipe.
    Slow (MediaPipe runs per __getitem__) but works without needing the
    dataset to ship pose json files.
    """

    def __init__(self, base_dataset):
        self.base_dataset = base_dataset

    def __len__(self):
        return len(self.base_dataset)

    def __getitem__(self, idx):
        item = self.base_dataset[idx]
        person_path = self.base_dataset.person_paths[idx]

        kps = extract_keypoints_mediapipe(person_path)
        if kps is None:
            kps = np.zeros((config.NUM_KEYPOINTS, 2), dtype=np.float32)

        # normalize to [-1, 1] to match config.IMG_SIZE resizing
        kps_norm = (kps / config.IMG_SIZE) * 2 - 1

        return item["person"], torch.tensor(kps_norm, dtype=torch.float32)


def train_pose_estimator(model, loader, epochs=config.POSE_EPOCHS,
                          lr=config.POSE_LR, device=config.DEVICE):
    model = model.to(device)
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)
    criterion = nn.MSELoss()

    for epoch in range(epochs):
        model.train()
        total_loss = 0.0

        for imgs, kps in loader:
            imgs, kps = imgs.to(device), kps.to(device)

            optimizer.zero_grad()
            pred = model(imgs)
            loss = criterion(pred, kps)
            loss.backward()
            optimizer.step()

            total_loss += loss.item() * imgs.size(0)

        print(f"[pose] epoch {epoch + 1}/{epochs} | loss: {total_loss / len(loader.dataset):.4f}")

    return model


def load_pose_model(checkpoint_path, device=config.DEVICE):
    model = PoseEstimator().to(device)
    model.load_state_dict(torch.load(checkpoint_path, map_location=device))
    model.eval()
    return model


if __name__ == "__main__":
    base_dataset = preprocessing.VTONDataset()
    pose_dataset = PoseDataset(base_dataset)
    loader = torch.utils.data.DataLoader(
        pose_dataset, batch_size=config.BATCH_SIZE, shuffle=True,
        num_workers=0,  # mediapipe is not fork-safe, keep workers=0
    )

    model = PoseEstimator()
    trained = train_pose_estimator(model, loader)

    ckpt_path = f"{config.CHECKPOINT_DIR}/pose_estimator.pth"
    torch.save(trained.state_dict(), ckpt_path)
    print(f"Saved pose estimator to {ckpt_path}")
