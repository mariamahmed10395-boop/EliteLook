# -*- coding: utf-8 -*-
"""
08_inference.py
=================
نقطة النهاية النهائية (Inference): بتاخد بيانات مستخدم جديد
وترجع:
  1) توقّع الموديل المدرّب للمقاس/الفيت المناسب.
  2) توصيات من محرك التشابه (أقرب مستخدمين شبهه).

طريقة التشغيل (مثال جاهز):
    python 08_inference.py

أو استورد الدالة predict_for_user() واستخدمها في تطبيقك.
"""

import joblib
import pandas as pd
import numpy as np

from config import (
    PREPROCESSOR_PATH,
    FINAL_MODEL_PATH,
)
from importlib import import_module

recommendation_module = import_module("07_recommendation_engine")


def load_inference_artifacts():
    preprocessor_bundle = joblib.load(PREPROCESSOR_PATH)
    model = joblib.load(FINAL_MODEL_PATH)
    return preprocessor_bundle, model


def predict_for_user(new_user: dict) -> dict:
    """
    بياخد dict فيه قياسات وتفضيلات مستخدم جديد، مثال:
        {
            "height": 170, "weight": 65, "chest": 90, "waist": 75,
            "hips": 95, "gender": "female", "fit_preference": "regular"
        }

    ويرجع dict فيه:
        - predicted_size: توقع الموديل المباشر
        - similar_users: أقرب مستخدمين شبهه من محرك التوصية
    """
    preprocessor_bundle, model = load_inference_artifacts()
    preprocessor = preprocessor_bundle["preprocessor"]
    numeric_cols = preprocessor_bundle["numeric_cols"]
    cat_cols = preprocessor_bundle["cat_cols"]

    # فهرس التشابه بيحتوي على reference_df للمساعدة في ملء القيم الناقصة
    sim_bundle = joblib.load(recommendation_module.SIMILARITY_INDEX_PATH)
    reference_df = sim_bundle["reference_df"]

    input_row = {}
    for col in numeric_cols + cat_cols:
        input_row[col] = new_user.get(col, np.nan)
    input_df = pd.DataFrame([input_row], dtype=object)

    for col in numeric_cols:
        if pd.isna(input_df.at[0, col]):
            input_df.at[0, col] = reference_df[col].median()
    for col in cat_cols:
        if pd.isna(input_df.at[0, col]) or input_df.at[0, col] is None:
            input_df.at[0, col] = reference_df[col].mode().iloc[0]

    input_transformed = preprocessor.transform(input_df)
    predicted_size = model.predict(input_transformed)[0]

    # احتمالات لكل فئة لو الموديل بيدعمها
    probabilities = None
    if hasattr(model, "predict_proba"):
        proba = model.predict_proba(input_transformed)[0]
        probabilities = dict(zip(model.classes_, proba.round(4).tolist()))

    similar_users = recommendation_module.recommend_for_user(new_user)

    return {
        "predicted_size": predicted_size,
        "class_probabilities": probabilities,
        "similar_users": similar_users,
    }


def main():
    # ---- عدّل القيم دي ببيانات المستخدم اللي عايز تجرب عليه ----
    example_user = {
        "height": 170,
        "weight": 65,
        "chest": 90,
        "waist": 75,
        "hips": 95,
        "gender": "female",
        "fit_preference": "regular",
    }

    print("[إدخال المستخدم]")
    print(example_user)

    result = predict_for_user(example_user)

    print("\n" + "=" * 60)
    print(f"المقاس/الفيت المتوقع: {result['predicted_size']}")
    if result["class_probabilities"]:
        print("احتمالات كل فئة:")
        for label, prob in result["class_probabilities"].items():
            print(f"   - {label}: {prob}")
    print("-" * 60)
    print("أقرب مستخدمين شبه المستخدم ده (للمقارنة/التوصية):")
    print(result["similar_users"])
    print("=" * 60)


if __name__ == "__main__":
    main()
