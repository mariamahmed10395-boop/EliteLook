"""
Stage 10 - Inference
Loads a trained VirtualTryOnPipeline checkpoint and runs it on a single
(person image, cloth image) pair, saving the final try-on result to disk.
This is the entry point end users / a demo app would call.

Usage:
    python 10_inference.py \
        --person path/to/person.jpg \
        --cloth path/to/cloth.jpg \
        --checkpoint checkpoints/tryon_latest.pth \
        --output outputs/result.png
"""

import argparse
import importlib

import torch
from PIL import Image

import config

preprocessing = importlib.import_module("02_data_preprocessing")
virtual_tryon = importlib.import_module("07_virtual_tryon")

VirtualTryOnPipeline = virtual_tryon.VirtualTryOnPipeline


def load_pipeline(checkpoint_path, device=config.DEVICE):
    pipeline = VirtualTryOnPipeline().to(device)
    pipeline.load_state_dict(torch.load(checkpoint_path, map_location=device))
    pipeline.eval()
    return pipeline


def load_image_tensor(path, device=config.DEVICE):
    img = Image.open(path).convert("RGB")
    tensor = preprocessing.base_transform(img).unsqueeze(0).to(device)
    return tensor


def tensor_to_pil(tensor):
    img = preprocessing.denormalize(tensor.squeeze(0).cpu()).clamp(0, 1)
    img = (img.permute(1, 2, 0).numpy() * 255).astype("uint8")
    return Image.fromarray(img)


def run_inference(person_path, cloth_path, checkpoint_path, output_path,
                   device=config.DEVICE):
    pipeline = load_pipeline(checkpoint_path, device)

    person = load_image_tensor(person_path, device)
    cloth = load_image_tensor(cloth_path, device)

    with torch.no_grad():
        result, warped_cloth, _ = pipeline(person, cloth)

    result_img = tensor_to_pil(result)
    result_img.save(output_path)

    warped_path = output_path.replace(".png", "_warped_cloth.png").replace(".jpg", "_warped_cloth.jpg")
    tensor_to_pil(warped_cloth).save(warped_path)

    print(f"Saved try-on result to: {output_path}")
    print(f"Saved warped cloth to : {warped_path}")

    return result_img


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--person", required=True, help="Path to the person image")
    parser.add_argument("--cloth", required=True, help="Path to the garment image")
    parser.add_argument(
        "--checkpoint",
        default=f"{config.CHECKPOINT_DIR}/tryon_latest.pth",
        help="Path to a saved VirtualTryOnPipeline state_dict",
    )
    parser.add_argument(
        "--output",
        default=f"{config.OUTPUT_DIR}/result.png",
        help="Where to save the final try-on image",
    )
    args = parser.parse_args()

    run_inference(args.person, args.cloth, args.checkpoint, args.output)
