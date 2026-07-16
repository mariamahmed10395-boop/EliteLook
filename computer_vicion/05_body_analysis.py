"""
Stage 05 - Body Analysis
Combines the segmentation mask (03) and pose keypoints (04) to estimate
rough body measurements (height, shoulder width, waist/hip width in pixels).
These are used as conditioning signals for garment warping (06) and can be
compared against the body_* columns present in similar HuggingFace/Kaggle
virtual try-on datasets.

Usage:
    python 05_body_analysis.py
"""

import importlib

import numpy as np
import torch

import config

preprocessing = importlib.import_module("02_data_preprocessing")
segmentation = importlib.import_module("03_segmentation")
pose_estimation = importlib.import_module("04_pose_estimation")

# MediaPipe pose landmark indices used for measurements
LEFT_SHOULDER, RIGHT_SHOULDER = 11, 12
LEFT_HIP, RIGHT_HIP = 23, 24
NOSE = 0
LEFT_ANKLE, RIGHT_ANKLE = 27, 28


def mask_bbox_height(mask_tensor):
    """
    mask_tensor: (1, H, W) tensor with values in [0, 1].
    Returns the pixel height of the bounding box of the segmented region.
    """
    mask = mask_tensor.squeeze(0).cpu().numpy() > 0.5
    rows = np.any(mask, axis=1)
    if not rows.any():
        return 0
    ymin, ymax = np.where(rows)[0][[0, -1]]
    return int(ymax - ymin)


def mask_width_at_row(mask_tensor, row_fraction):
    """
    Returns the horizontal width (in pixels) of the segmented region at a
    given normalized row (0 = top, 1 = bottom). Used to approximate
    shoulder / waist / hip width.
    """
    mask = mask_tensor.squeeze(0).cpu().numpy() > 0.5
    h = mask.shape[0]
    row = int(row_fraction * (h - 1))
    cols = np.where(mask[row])[0]
    if len(cols) == 0:
        return 0
    return int(cols[-1] - cols[0])


def estimate_body_measurements(mask_tensor, keypoints=None):
    """
    Returns a dict with rough pixel-space measurements:
        height, shoulder_width, waist_width, hip_width
    If keypoints are provided (from 04_pose_estimation), shoulder/hip rows
    are located precisely; otherwise fixed row fractions are used as a
    fallback approximation.
    """
    height = mask_bbox_height(mask_tensor)

    if keypoints is not None and keypoints.shape[0] > max(LEFT_HIP, RIGHT_HIP):
        img_h = config.IMG_SIZE
        shoulder_row_frac = float(
            (keypoints[LEFT_SHOULDER, 1] + keypoints[RIGHT_SHOULDER, 1]) / 2
        ) / img_h
        hip_row_frac = float(
            (keypoints[LEFT_HIP, 1] + keypoints[RIGHT_HIP, 1]) / 2
        ) / img_h
        waist_row_frac = (shoulder_row_frac + hip_row_frac) / 2
    else:
        # fallback fixed proportions of a standing full-body photo
        shoulder_row_frac = 0.20
        waist_row_frac = 0.45
        hip_row_frac = 0.55

    shoulder_row_frac = min(max(shoulder_row_frac, 0.0), 1.0)
    waist_row_frac = min(max(waist_row_frac, 0.0), 1.0)
    hip_row_frac = min(max(hip_row_frac, 0.0), 1.0)

    return {
        "height_px": height,
        "shoulder_width_px": mask_width_at_row(mask_tensor, shoulder_row_frac),
        "waist_width_px": mask_width_at_row(mask_tensor, waist_row_frac),
        "hip_width_px": mask_width_at_row(mask_tensor, hip_row_frac),
    }


def pixels_to_cm(pixel_value, reference_height_px, reference_height_cm=170.0):
    """
    Naive pixel-to-centimeter conversion using a reference height.
    Only meaningful if the person roughly fills the frame; replace with a
    calibrated camera model for production use.
    """
    if reference_height_px == 0:
        return 0.0
    return pixel_value * (reference_height_cm / reference_height_px)


def analyze_batch(person_imgs, masks, keypoints_batch=None):
    """
    Runs estimate_body_measurements over a batch.
    person_imgs: (B, 3, H, W) - unused directly, kept for future extensions
    masks: (B, 1, H, W)
    keypoints_batch: optional (B, N, 2)
    Returns a list of measurement dicts, one per sample.
    """
    results = []
    for i in range(masks.size(0)):
        kps = keypoints_batch[i].cpu().numpy() if keypoints_batch is not None else None
        results.append(estimate_body_measurements(masks[i], kps))
    return results


if __name__ == "__main__":
    dataset = preprocessing.VTONDataset()
    loader = preprocessing.get_dataloader(dataset, batch_size=4, shuffle=False)
    batch = next(iter(loader))

    if "mask" not in batch:
        raise RuntimeError(
            "This demo needs ground-truth masks. Either provide config.MASK_DIR "
            "or run 03_segmentation.py first and predict masks on the fly."
        )

    measurements = analyze_batch(batch["person"], batch["mask"])
    for fname, m in zip(batch["filename"], measurements):
        print(fname, m)
