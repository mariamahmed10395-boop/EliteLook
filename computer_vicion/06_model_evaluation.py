# -*- coding: utf-8 -*-
"""
06_model_evaluation.py
========================
تقييم شامل للموديل النهائي: accuracy, precision, recall, f1,
confusion matrix، وحفظ تقرير JSON.

طريقة التشغيل:
    python 06_model_evaluation.py
"""

import json
import joblib
import numpy as np
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix,
)

from config import (
    TRAIN_TEST_SPLIT_PATH,
    FINAL_MODEL_PATH,
    EVALUATION_REPORT_PATH,
)


def load_artifacts():
    split = joblib.load(TRAIN_TEST_SPLIT_PATH)
    model = joblib.load(FINAL_MODEL_PATH)
    return split, model


def main():
    split, model = load_artifacts()
    X_test, y_test = split["X_test"], split["y_test"]

    preds = model.predict(X_test)

    accuracy = accuracy_score(y_test, preds)
    precision = precision_score(y_test, preds, average="weighted", zero_division=0)
    recall = recall_score(y_test, preds, average="weighted", zero_division=0)
    f1 = f1_score(y_test, preds, average="weighted", zero_division=0)
    report = classification_report(y_test, preds, zero_division=0, output_dict=True)
    cm = confusion_matrix(y_test, preds).tolist()
    labels = sorted(np.unique(y_test).tolist())

    print("=" * 60)
    print(f"Accuracy : {accuracy:.4f}")
    print(f"Precision (weighted): {precision:.4f}")
    print(f"Recall (weighted)   : {recall:.4f}")
    print(f"F1-score (weighted) : {f1:.4f}")
    print("-" * 60)
    print("تقرير التصنيف التفصيلي:")
    print(classification_report(y_test, preds, zero_division=0))
    print("-" * 60)
    print(f"مصفوفة الالتباس (Confusion Matrix) - الترتيب حسب: {labels}")
    print(np.array(cm))
    print("=" * 60)

    # أهمية الفيتشرز لو الموديل بيدعمها (RandomForest بيدعمها)
    feature_importances = None
    if hasattr(model, "feature_importances_"):
        feature_importances = model.feature_importances_.tolist()

    report_dict = {
        "accuracy": accuracy,
        "precision_weighted": precision,
        "recall_weighted": recall,
        "f1_weighted": f1,
        "labels": labels,
        "confusion_matrix": cm,
        "classification_report": report,
        "feature_importances": feature_importances,
    }

    with open(EVALUATION_REPORT_PATH, "w", encoding="utf-8") as f:
        json.dump(report_dict, f, ensure_ascii=False, indent=2)

    print(f"\n[تم] تقرير التقييم اتحفظ في: {EVALUATION_REPORT_PATH}")


if __name__ == "__main__":
    main()
