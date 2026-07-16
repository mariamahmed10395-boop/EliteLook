# -*- coding: utf-8 -*-
"""
03_feature_engineering.py
==========================
بناء فيتشرز جديدة مفيدة لمشكلة التوصية بالمقاس/الفيت المناسب:
- BMI
- نسب جسدية (waist-to-hip, chest-to-waist ... إلخ لو الأعمدة متاحة)
- ترميز الأعمدة التصنيفية (One-Hot Encoding)
- تحجيم الأعمدة الرقمية (Scaling)

طريقة التشغيل:
    python 03_feature_engineering.py
"""

import pandas as pd
import numpy as np
import joblib
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer

from config import (
    CLEANED_DATA_PATH,
    FEATURED_DATA_PATH,
    PREPROCESSOR_PATH,
    BODY_MEASUREMENT_COLUMNS,
    CATEGORICAL_COLUMNS,
    TARGET_COLUMN,
)


def load_data() -> pd.DataFrame:
    return pd.read_pickle(CLEANED_DATA_PATH)


def get_existing_columns(df: pd.DataFrame, columns: list) -> list:
    return [c for c in columns if c in df.columns]


def add_body_ratio_features(df: pd.DataFrame) -> pd.DataFrame:
    """يضيف فيتشرز مشتقة من القياسات الجسدية لو الأعمدة الأساسية موجودة."""
    cols = df.columns

    # BMI = weight(kg) / height(m)^2
    if "weight" in cols and "height" in cols:
        height_m = df["height"] / 100.0 if df["height"].median() > 3 else df["height"]
        df["bmi"] = df["weight"] / (height_m ** 2)

    if "waist" in cols and "hips" in cols:
        df["waist_to_hip_ratio"] = df["waist"] / df["hips"].replace(0, np.nan)

    if "chest" in cols and "waist" in cols:
        df["chest_to_waist_ratio"] = df["chest"] / df["waist"].replace(0, np.nan)

    if "shoulder_width" in cols and "height" in cols:
        df["shoulder_to_height_ratio"] = df["shoulder_width"] / df["height"].replace(0, np.nan)

    # أي قيم NaN/inf ناتجة عن القسمة نستبدلها بالـ median
    new_ratio_cols = [
        c for c in [
            "bmi", "waist_to_hip_ratio", "chest_to_waist_ratio", "shoulder_to_height_ratio"
        ] if c in df.columns
    ]
    for col in new_ratio_cols:
        df[col] = df[col].replace([np.inf, -np.inf], np.nan)
        df[col] = df[col].fillna(df[col].median())

    if new_ratio_cols:
        print(f"[فيتشرز جديدة] اتضافت: {new_ratio_cols}")

    return df


def build_preprocessor(numeric_cols: list, cat_cols: list) -> ColumnTransformer:
    """يبني ColumnTransformer بيعمل scaling للأرقام وone-hot للتصنيفي، عشان يتحفظ ويُستخدم لاحقًا في inference."""
    preprocessor = ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), numeric_cols),
            ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), cat_cols),
        ],
        remainder="drop",
    )
    return preprocessor


def main() -> pd.DataFrame:
    df = load_data()
    df = add_body_ratio_features(df)

    base_numeric = get_existing_columns(df, BODY_MEASUREMENT_COLUMNS)
    derived_numeric = [
        c for c in ["bmi", "waist_to_hip_ratio", "chest_to_waist_ratio", "shoulder_to_height_ratio"]
        if c in df.columns
    ]
    numeric_cols = base_numeric + derived_numeric

    cat_cols = get_existing_columns(df, CATEGORICAL_COLUMNS)

    if not numeric_cols:
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        numeric_cols = [c for c in numeric_cols if c != TARGET_COLUMN]
    if not cat_cols:
        cat_cols = df.select_dtypes(include=["object"]).columns.tolist()
        cat_cols = [c for c in cat_cols if c != TARGET_COLUMN]

    print(f"الأعمدة الرقمية المستخدمة: {numeric_cols}")
    print(f"الأعمدة التصنيفية المستخدمة: {cat_cols}")

    preprocessor = build_preprocessor(numeric_cols, cat_cols)

    # بنفيت الـ preprocessor على الداتا (بدون التارجت) عشان نتأكد إنه شغال، وبنحفظه
    feature_df = df[numeric_cols + cat_cols]
    preprocessor.fit(feature_df)

    joblib.dump(
        {"preprocessor": preprocessor, "numeric_cols": numeric_cols, "cat_cols": cat_cols},
        PREPROCESSOR_PATH,
    )
    print(f"[تم] الـ preprocessor اتحفظ في: {PREPROCESSOR_PATH}")

    # بنحفظ الداتا بعد إضافة الفيتشرز (لسه من غير transform نهائي، عشان نحتفظ بالأعمدة الأصلية للـ evaluation/recommendation)
    df.to_pickle(FEATURED_DATA_PATH)
    print(f"[تم] الداتا بعد الفيتشر إنجينيرنج اتحفظت في: {FEATURED_DATA_PATH}")
    print(f"الشكل النهائي: {df.shape}")
    return df


if __name__ == "__main__":
    main()
