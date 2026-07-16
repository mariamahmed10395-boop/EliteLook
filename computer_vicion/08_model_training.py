"""
Stage 08 - Model Training
Trains the full VirtualTryOnPipeline (warper + generator) adversarially
against the PatchDiscriminator, defined in 07_virtual_tryon.py.
Used only during development; the shipped artifact is the checkpoint file
consumed by 10_inference.py.

Usage:
    python 08_model_training.py
"""

import importlib
import os
import time

import torch
import torch.nn as nn

import config

preprocessing = importlib.import_module("02_data_preprocessing")
virtual_tryon = importlib.import_module("07_virtual_tryon")

VirtualTryOnPipeline = virtual_tryon.VirtualTryOnPipeline
PatchDiscriminator = virtual_tryon.PatchDiscriminator


def train(
    epochs=config.TRYON_EPOCHS,
    lr=config.TRYON_LR,
    l1_weight=config.L1_LOSS_WEIGHT,
    device=config.DEVICE,
    checkpoint_every=5,
):
    dataset = preprocessing.VTONDataset()
    loader = preprocessing.get_dataloader(dataset)

    pipeline = VirtualTryOnPipeline().to(device)
    discriminator = PatchDiscriminator().to(device)

    opt_g = torch.optim.Adam(pipeline.parameters(), lr=lr, betas=(0.5, 0.999))
    opt_d = torch.optim.Adam(discriminator.parameters(), lr=lr, betas=(0.5, 0.999))

    adv_criterion = nn.BCEWithLogitsLoss()
    l1_criterion = nn.L1Loss()

    for epoch in range(epochs):
        start = time.time()
        epoch_loss_g, epoch_loss_d = 0.0, 0.0
        n_batches = 0

        for batch in loader:
            person = batch["person"].to(device)
            cloth = batch["cloth"].to(device)
            real_img = person  # paired dataset: target is the person already wearing the cloth

            # ---------------- Discriminator step ----------------
            opt_d.zero_grad()
            with torch.no_grad():
                fake_img, warped_cloth, _ = pipeline(person, cloth)

            pred_real = discriminator(person, cloth, real_img)
            pred_fake = discriminator(person, cloth, fake_img)

            loss_d = 0.5 * (
                adv_criterion(pred_real, torch.ones_like(pred_real))
                + adv_criterion(pred_fake, torch.zeros_like(pred_fake))
            )
            loss_d.backward()
            opt_d.step()

            # ---------------- Generator step ----------------
            opt_g.zero_grad()
            fake_img, warped_cloth, _ = pipeline(person, cloth)
            pred_fake = discriminator(person, cloth, fake_img)

            loss_g_adv = adv_criterion(pred_fake, torch.ones_like(pred_fake))
            loss_g_l1 = l1_criterion(fake_img, real_img) * l1_weight

            if "mask" in batch:
                warp_target = real_img * batch["mask"].to(device)
            else:
                warp_target = real_img
            loss_warp_l1 = l1_criterion(warped_cloth, warp_target) * 10

            loss_g = loss_g_adv + loss_g_l1 + loss_warp_l1
            loss_g.backward()
            opt_g.step()

            epoch_loss_g += loss_g.item()
            epoch_loss_d += loss_d.item()
            n_batches += 1

        elapsed = time.time() - start
        print(
            f"[training] epoch {epoch + 1}/{epochs} | "
            f"G: {epoch_loss_g / n_batches:.4f} | "
            f"D: {epoch_loss_d / n_batches:.4f} | "
            f"{elapsed:.1f}s"
        )

        if (epoch + 1) % checkpoint_every == 0 or (epoch + 1) == epochs:
            save_checkpoint(pipeline, discriminator, opt_g, opt_d, epoch + 1)

    return pipeline, discriminator


def save_checkpoint(pipeline, discriminator, opt_g, opt_d, epoch):
    path = os.path.join(config.CHECKPOINT_DIR, f"tryon_epoch{epoch}.pth")
    torch.save(
        {
            "epoch": epoch,
            "pipeline_state_dict": pipeline.state_dict(),
            "discriminator_state_dict": discriminator.state_dict(),
            "opt_g_state_dict": opt_g.state_dict(),
            "opt_d_state_dict": opt_d.state_dict(),
        },
        path,
    )
    print(f"[training] checkpoint saved: {path}")

    # also keep a stable "latest" pointer for 09/10 to consume
    latest_path = os.path.join(config.CHECKPOINT_DIR, "tryon_latest.pth")
    torch.save(pipeline.state_dict(), latest_path)


if __name__ == "__main__":
    train()
