"""
Stage 09 - Model Evaluation
Computes quantitative image-quality metrics (L1, PSNR, SSIM) for a trained
VirtualTryOnPipeline checkpoint against the held-out portion of the dataset.

Usage:
    python 09_model_evaluation.py --checkpoint checkpoints/tryon_latest.pth
"""

import argparse
import importlib

import numpy as np
import torch
import torch.nn.functional as F

import config

preprocessing = importlib.import_module("02_data_preprocessing")
virtual_tryon = importlib.import_module("07_virtual_tryon")

VirtualTryOnPipeline = virtual_tryon.VirtualTryOnPipeline

try:
    from skimage.metrics import structural_similarity as ssim
    _HAS_SKIMAGE = True
except ImportError:
    _HAS_SKIMAGE = False


def compute_l1(fake, real):
    return F.l1_loss(fake, real).item()


def compute_psnr(fake, real, max_val=2.0):
    # tensors are in [-1, 1], so the dynamic range is 2.0
    mse = F.mse_loss(fake, real).item()
    if mse == 0:
        return float("inf")
    return 20 * np.log10(max_val) - 10 * np.log10(mse)


def compute_ssim(fake, real):
    if not _HAS_SKIMAGE:
        return None

    fake_np = preprocessing.denormalize(fake).cpu().permute(0, 2, 3, 1).numpy()
    real_np = preprocessing.denormalize(real).cpu().permute(0, 2, 3, 1).numpy()

    scores = []
    for f_img, r_img in zip(fake_np, real_np):
        score = ssim(f_img, r_img, channel_axis=2, data_range=1.0)
        scores.append(score)
    return float(np.mean(scores))


def evaluate(checkpoint_path, device=config.DEVICE, max_batches=None):
    dataset = preprocessing.VTONDataset()
    loader = preprocessing.get_dataloader(dataset, shuffle=False)

    pipeline = VirtualTryOnPipeline().to(device)
    pipeline.load_state_dict(torch.load(checkpoint_path, map_location=device))
    pipeline.eval()

    l1_scores, psnr_scores, ssim_scores = [], [], []

    with torch.no_grad():
        for i, batch in enumerate(loader):
            if max_batches is not None and i >= max_batches:
                break

            person = batch["person"].to(device)
            cloth = batch["cloth"].to(device)
            real_img = person

            fake_img, _, _ = pipeline(person, cloth)

            l1_scores.append(compute_l1(fake_img, real_img))
            psnr_scores.append(compute_psnr(fake_img, real_img))

            s = compute_ssim(fake_img, real_img)
            if s is not None:
                ssim_scores.append(s)

    results = {
        "L1": float(np.mean(l1_scores)),
        "PSNR": float(np.mean(psnr_scores)),
    }
    if ssim_scores:
        results["SSIM"] = float(np.mean(ssim_scores))
    else:
        results["SSIM"] = "skipped (install scikit-image to enable)"

    return results


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--checkpoint",
        default=f"{config.CHECKPOINT_DIR}/tryon_latest.pth",
        help="Path to a saved VirtualTryOnPipeline state_dict",
    )
    parser.add_argument(
        "--max-batches",
        type=int,
        default=None,
        help="Optionally limit evaluation to N batches for a quick check",
    )
    args = parser.parse_args()

    metrics = evaluate(args.checkpoint, max_batches=args.max_batches)
    print("Evaluation results:")
    for name, value in metrics.items():
        print(f"  {name}: {value}")
