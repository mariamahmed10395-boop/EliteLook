# -*- coding: utf-8 -*-
"""
05_model_tuning.py
====================
تحسين الموديل عن طريق البحث عن أفضل الـ hyperparameters باستخدام
RandomizedSearchCV، وحفظ أفضل موديل كـ "final_model".

طريقة التشغيل:
    python 05_model_tuning.py
"""

import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import RandomizedSearchCV
from sklearn.metrics import accuracy_score, f1_score

from config import (
    TRAIN_TEST_SPLIT_PATH,
    TUNED_MODEL_PATH,
    FINAL_MODEL_PATH,
    RANDOM_STATE,
)


PARAM_DISTRIBUTIONS = {
    "n_estimators": [100, 200, 300, 400, 500],
    "max_depth": [None, 5, 10, 15, 20, 30],
    "min_samples_split": [2, 4, 6, 10],
    "min_samples_leaf": [1, 2, 4, 6],
    "max_features": ["sqrt", "log2", None],
    "class_weight": [None, "balanced"],
}


def load_split():
    return joblib.load(TRAIN_TEST_SPLIT_PATH)


def main():
    split = load_split()
    X_train, X_test = split["X_train"], split["X_test"]
    y_train, y_test = split["y_train"], split["y_test"]

    base_model = RandomForestClassifier(random_state=RANDOM_STATE, n_jobs=-1)

    search = RandomizedSearchCV(
        estimator=base_model,
        param_distributions=PARAM_DISTRIBUTIONS,
        n_iter=25,
        scoring="f1_weighted",
        cv=5,
        random_state=RANDOM_STATE,
        n_jobs=-1,
        verbose=1,
    )

    print("[جاري البحث] بندور على أفضل إعدادات للموديل (ده ممكن ياخد شوية وقت)...")
    search.fit(X_train, y_train)

    print(f"\nأفضل إعدادات: {search.best_params_}")
    print(f"أفضل نتيجة CV (f1_weighted): {search.best_score_:.4f}")

    best_model = search.best_estimator_

    test_preds = best_model.predict(X_test)
    print(f"دقة الاختبار بعد الضبط: {accuracy_score(y_test, test_preds):.4f}")
    print(f"F1-score (weighted) بعد الضبط: {f1_score(y_test, test_preds, average='weighted'):.4f}")

    joblib.dump(best_model, TUNED_MODEL_PATH)
    joblib.dump(best_model, FINAL_MODEL_PATH)
    print(f"\n[تم] أفضل موديل اتحفظ في: {TUNED_MODEL_PATH}")
    print(f"[تم] نفس الموديل اتحفظ كموديل نهائي في: {FINAL_MODEL_PATH}")


if __name__ == "__main__":
    main()
