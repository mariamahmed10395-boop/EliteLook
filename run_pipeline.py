"""
Runs every pipeline stage end to end, in order, executing each stage's own
`if __name__ == "__main__"` block via runpy. Individual stages can still be
run/debugged independently, e.g.:
    python 03_segmentation.py

Usage:
    python run_pipeline.py
"""

import runpy

STAGES = [
    "01_data_loading",
    "02_data_preprocessing",
    "03_segmentation",
    "04_pose_estimation",
    "05_body_analysis",
    "06_garment_processing",
    "07_virtual_tryon",
    "08_model_training",
    "09_model_evaluation",
    # 10_inference is intentionally excluded here: it needs explicit
    # --person / --cloth arguments and is meant to be called on demand,
    # e.g. `python 10_inference.py --person p.jpg --cloth c.jpg`
]

if __name__ == "__main__":
    for stage in STAGES:
        print(f"\n{'=' * 60}\nRunning stage: {stage}\n{'=' * 60}")
        runpy.run_module(stage, run_name="__main__")
