# -*- coding: utf-8 -*-
"""
04_model_training.py
=====================
تدريب موديل أساسي (Baseline) للتنبؤ بعمود الهدف (مثلاً: المقاس المناسب / الفيت).

طريقة التشغيل:
    python 04_model_training.py
"""

import sys
import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score

from config import (
    FEATURED_DATA_PATH,
    PREPROCESSOR_PATH,
    TRAIN_TEST_SPLIT_PATH,
    BASELINE_MODEL_PATH,
    FINAL_MODEL_PATH,
    TARGET_COLUMN,
    TEST_SIZE,
    RANDOM_STATE,
)


CANDIDATE_TARGET_NAMES = [
    TARGET_COLUMN, "recommended_size", "size", "fit", "fit_score",
    "garment_fit_score", "size_label", "target",
]


def resolve_target_column(df: pd.DataFrame) -> str:
    """يحاول يلاقي عمود الهدف الصحيح لو الاسم في config.py مش مطابق 100%."""
    for name in CANDIDATE_TARGET_NAMES:
        if name in df.columns:
            return name
    sys.exit(
        "[خطأ] معرفناش نلاقي عمود الهدف (target) في الداتا.\n"
        f"الأعمدة المتاحة: {list(df.columns)}\n"
        "افتح config.py وعدّل قيمة TARGET_COLUMN بالاسم الصحيح لعمود "
        "المقاس/الفيت اللي عايز تتنبأ بيه."
    )


def load_data():
    df = pd.read_pickle(FEATURED_DATA_PATH)
    bundle = joblib.load(PREPROCESSOR_PATH)
    return df, bundle


def main():
    df, bundle = load_data()
    preprocessor = bundle["preprocessor"]
    numeric_cols = bundle["numeric_cols"]
    cat_cols = bundle["cat_cols"]

    target_col = resolve_target_column(df)
    print(f"[هدف التدريب] عمود الهدف المستخدم: '{target_col}'")

    X = df[numeric_cols + cat_cols]
    y = df[target_col].astype(str)

    X_transformed = preprocessor.transform(X)

    X_train, X_test, y_train, y_test = train_test_split(
        X_transformed, y,
        test_size=TEST_SIZE,
        random_state=RANDOM_STATE,
        stratify=y if y.nunique() > 1 else None,
    )

    joblib.dump(
        {
            "X_train": X_train, "X_test": X_test,
            "y_train": y_train, "y_test": y_test,
            "target_col": target_col,
        },
        TRAIN_TEST_SPLIT_PATH,
    )

    model = RandomForestClassifier(
        n_estimators=200,
        random_state=RANDOM_STATE,
        n_jobs=-1,
    )
    model.fit(X_train, y_train)

    train_preds = model.predict(X_train)
    test_preds = model.predict(X_test)

    print(f"دقة التدريب (Train Accuracy): {accuracy_score(y_train, train_preds):.4f}")
    print(f"دقة الاختبار (Test Accuracy): {accuracy_score(y_test, test_preds):.4f}")
    print(f"F1-score (weighted) على الاختبار: {f1_score(y_test, test_preds, average='weighted'):.4f}")

    joblib.dump(model, BASELINE_MODEL_PATH)
    # بنحفظه كمان كـ "final_model" مبدئيًا عشان باقي الخطوات (evaluation/inference)
    # تلاقي موديل جاهز حتى لو لسه معملتش تشغيل خطوة الـ tuning (05).
    # لما تشغّل 05_model_tuning.py هيستبدله بأفضل موديل بعد الضبط.
    joblib.dump(model, FINAL_MODEL_PATH)
    print(f"\n[تم] الموديل الأساسي اتحفظ في: {BASELINE_MODEL_PATH}")
    print(f"[تم] نفس الموديل اتحفظ مبدئيًا كموديل نهائي في: {FINAL_MODEL_PATH}")


if __name__ == "__main__":
    main()
