# -*- coding: utf-8 -*-
"""
run_all.py
==========
بيشغل كل خطوات الـ pipeline بالترتيب دفعة واحدة (من غير model tuning
اللي بياخد وقت أطول - شغّله لوحده لو محتاجه).

طريقة التشغيل:
    python run_all.py
"""

import runpy

STEPS = [
    "01_data_loading.py",
    "02_data_preprocessing.py",
    "03_feature_engineering.py",
    "04_model_training.py",
    "06_model_evaluation.py",
    "07_recommendation_engine.py",
    "08_inference.py",
]

# ملحوظة: 05_model_tuning.py متعمول استبعاده من التشغيل التلقائي لأنه
# بياخد وقت أطول (Grid/Randomized Search). شغّله لوحده لما تحتاج تحسين الموديل:
#     python 05_model_tuning.py


def main():
    for step in STEPS:
        print("\n" + "#" * 70)
        print(f"# جاري تشغيل: {step}")
        print("#" * 70 + "\n")
        runpy.run_path(step, run_name="__main__")


if __name__ == "__main__":
    main()
