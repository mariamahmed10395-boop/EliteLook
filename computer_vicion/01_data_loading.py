# -*- coding: utf-8 -*-
"""
01_data_loading.py
===================
تحميل بيانات الداتاست (Personalized Clothing & Body Measurements Data)
والتأكد من سلامتها الأساسية، ثم حفظها كـ pickle عشان الخطوة الجاية تستخدمها.

طريقة التشغيل:
    python 01_data_loading.py
"""

import sys
import pandas as pd

from config import RAW_DATA_PATH, LOADED_DATA_PATH


def load_raw_data(path: str = RAW_DATA_PATH) -> pd.DataFrame:
    """يحمل ملف الـ CSV الخام ويرجعه كـ DataFrame."""
    try:
        df = pd.read_csv(path)
    except FileNotFoundError:
        sys.exit(
            f"[خطأ] الملف مش موجود: {path}\n"
            "حمّل الداتاست من كاجل وحطه في مجلد data/ باسم raw_data.csv\n"
            "الرابط: https://www.kaggle.com/datasets/zara2099/"
            "personalized-clothing-and-body-measurements-data"
        )
    return df


def inspect_data(df: pd.DataFrame) -> None:
    """يطبع نظرة سريعة على الداتا (شكل، أعمدة، نواقص، عينة)."""
    print("=" * 60)
    print(f"عدد الصفوف والأعمدة: {df.shape}")
    print("-" * 60)
    print("أسماء الأعمدة:")
    print(list(df.columns))
    print("-" * 60)
    print("أنواع البيانات:")
    print(df.dtypes)
    print("-" * 60)
    print("القيم الناقصة لكل عمود:")
    print(df.isnull().sum())
    print("-" * 60)
    print("عينة من الداتا:")
    print(df.head())
    print("=" * 60)


def basic_sanity_checks(df: pd.DataFrame) -> None:
    """تحققات بسيطة: صفوف مكررة، أعمدة فاضية بالكامل."""
    n_dupes = df.duplicated().sum()
    if n_dupes:
        print(f"[تنبيه] فيه {n_dupes} صف مكرر في الداتا.")

    empty_cols = [c for c in df.columns if df[c].isnull().all()]
    if empty_cols:
        print(f"[تنبيه] الأعمدة دي فاضية بالكامل: {empty_cols}")


def main() -> pd.DataFrame:
    df = load_raw_data()
    inspect_data(df)
    basic_sanity_checks(df)

    df.to_pickle(LOADED_DATA_PATH)
    print(f"\n[تم] الداتا اتحفظت في: {LOADED_DATA_PATH}")
    return df


if __name__ == "__main__":
    main()
