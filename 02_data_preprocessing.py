# -*- coding: utf-8 -*-
"""
02_data_preprocessing.py
=========================
تنظيف الداتا: التعامل مع القيم الناقصة، إزالة التكرار، تصحيح الأنواع،
وتجهيزها للخطوة الجاية (feature engineering).

طريقة التشغيل:
    python 02_data_preprocessing.py
"""

import pandas as pd
import numpy as np

from config import (
    LOADED_DATA_PATH,
    CLEANED_DATA_PATH,
    BODY_MEASUREMENT_COLUMNS,
    CATEGORICAL_COLUMNS,
    ID_COLUMNS,
)


def load_data() -> pd.DataFrame:
    return pd.read_pickle(LOADED_DATA_PATH)


def get_existing_columns(df: pd.DataFrame, columns: list) -> list:
    """يرجع بس الأعمدة الموجودة فعليًا في الداتا (تفادي أي اختلاف بسيط بالأسماء)."""
    existing = [c for c in columns if c in df.columns]
    missing = [c for c in columns if c not in df.columns]
    if missing:
        print(f"[ملاحظة] الأعمدة دي مش موجودة في الداتا وهيتم تجاهلها: {missing}")
    return existing


def drop_id_and_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    df = df.drop_duplicates().reset_index(drop=True)
    id_cols = get_existing_columns(df, ID_COLUMNS)
    if id_cols:
        df = df.drop(columns=id_cols)
    return df


def handle_missing_numeric(df: pd.DataFrame, numeric_cols: list) -> pd.DataFrame:
    """يملأ القيم الناقصة في الأعمدة الرقمية بالـ median."""
    for col in numeric_cols:
        if df[col].isnull().any():
            median_val = df[col].median()
            df[col] = df[col].fillna(median_val)
    return df


def handle_missing_categorical(df: pd.DataFrame, cat_cols: list) -> pd.DataFrame:
    """يملأ القيم الناقصة في الأعمدة التصنيفية بالـ mode (الأكثر تكرارًا)."""
    for col in cat_cols:
        if df[col].isnull().any():
            mode_val = df[col].mode(dropna=True)
            fill_val = mode_val.iloc[0] if not mode_val.empty else "unknown"
            df[col] = df[col].fillna(fill_val)
    return df


def remove_outliers_iqr(df: pd.DataFrame, numeric_cols: list, factor: float = 3.0) -> pd.DataFrame:
    """يشيل القيم الشاذة الواضحة في الأعمدة الرقمية باستخدام IQR (متسامح: factor=3)."""
    for col in numeric_cols:
        q1 = df[col].quantile(0.25)
        q3 = df[col].quantile(0.75)
        iqr = q3 - q1
        if iqr == 0:
            continue
        lower = q1 - factor * iqr
        upper = q3 + factor * iqr
        before = len(df)
        df = df[(df[col] >= lower) & (df[col] <= upper)]
        removed = before - len(df)
        if removed:
            print(f"[تنظيف] اتشال {removed} صف شاذ من عمود '{col}'.")
    return df.reset_index(drop=True)


def standardize_categorical_text(df: pd.DataFrame, cat_cols: list) -> pd.DataFrame:
    """توحيد شكل النصوص (مسافات زيادة، حروف كبيرة/صغيرة)."""
    for col in cat_cols:
        df[col] = df[col].astype(str).str.strip().str.lower()
    return df


def main() -> pd.DataFrame:
    df = load_data()
    df = drop_id_and_duplicates(df)

    numeric_cols = get_existing_columns(df, BODY_MEASUREMENT_COLUMNS)
    cat_cols = get_existing_columns(df, CATEGORICAL_COLUMNS)

    # لو الأعمدة معرفتش تتلاقى بالاسم، نحاول نكتشفها تلقائيًا كخطة بديلة
    if not numeric_cols:
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        print(f"[اكتشاف تلقائي] استخدمنا الأعمدة الرقمية دي: {numeric_cols}")
    if not cat_cols:
        cat_cols = df.select_dtypes(include=["object"]).columns.tolist()
        print(f"[اكتشاف تلقائي] استخدمنا الأعمدة التصنيفية دي: {cat_cols}")

    df = handle_missing_numeric(df, numeric_cols)
    df = handle_missing_categorical(df, cat_cols)
    df = standardize_categorical_text(df, cat_cols)
    df = remove_outliers_iqr(df, numeric_cols)

    df.to_pickle(CLEANED_DATA_PATH)
    print(f"\n[تم] الداتا بعد التنظيف اتحفظت في: {CLEANED_DATA_PATH}")
    print(f"الشكل النهائي: {df.shape}")
    return df


if __name__ == "__main__":
    main()
