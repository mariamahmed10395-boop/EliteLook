# -*- coding: utf-8 -*-
"""
07_recommendation_engine.py
=============================
محرك توصية بيعتمد على تشابه المستخدمين (Content-Based / KNN):
بياخد قياسات جسم مستخدم جديد ويلاقي أقرب المستخدمين ليه في الداتا،
وبيرجع المقاسات/التفضيلات اللي مناسبالهم كتوصية.

طريقة التشغيل:
    python 07_recommendation_engine.py
"""

import joblib
import pandas as pd
import numpy as np
from sklearn.neighbors import NearestNeighbors

from config import (
    FEATURED_DATA_PATH,
    PREPROCESSOR_PATH,
    SIMILARITY_INDEX_PATH,
    TARGET_COLUMN,
    N_RECOMMENDATIONS,
)
from importlib import import_module

# بنستعير نفس دالة اكتشاف عمود الهدف من ملف التدريب عشان نفس المنطق يتكرر
training_module = import_module("04_model_training")


def build_similarity_index():
    df = pd.read_pickle(FEATURED_DATA_PATH)
    bundle = joblib.load(PREPROCESSOR_PATH)
    preprocessor = bundle["preprocessor"]
    numeric_cols = bundle["numeric_cols"]
    cat_cols = bundle["cat_cols"]

    target_col = training_module.resolve_target_column(df)

    X = df[numeric_cols + cat_cols]
    X_transformed = preprocessor.transform(X)

    knn = NearestNeighbors(n_neighbors=N_RECOMMENDATIONS, metric="euclidean")
    knn.fit(X_transformed)

    joblib.dump(
        {
            "knn": knn,
            "reference_df": df.reset_index(drop=True),
            "target_col": target_col,
            "numeric_cols": numeric_cols,
            "cat_cols": cat_cols,
        },
        SIMILARITY_INDEX_PATH,
    )
    print(f"[تم] فهرس التشابه (Similarity Index) اتحفظ في: {SIMILARITY_INDEX_PATH}")
    return knn, df, target_col


def recommend_for_user(new_user: dict, top_n: int = N_RECOMMENDATIONS) -> pd.DataFrame:
    """
    بياخد قياسات مستخدم جديد كـ dict (نفس أسماء الأعمدة الأصلية)
    ويرجع أقرب top_n مستخدمين شبهه مع المقاس/التوصية بتاعتهم.

    مثال:
        recommend_for_user({
            "height": 170, "weight": 65, "chest": 90, "waist": 75,
            "hips": 95, "gender": "female", "fit_preference": "regular"
        })
    """
    bundle = joblib.load(SIMILARITY_INDEX_PATH)
    knn = bundle["knn"]
    reference_df = bundle["reference_df"]
    target_col = bundle["target_col"]
    numeric_cols = bundle["numeric_cols"]
    cat_cols = bundle["cat_cols"]

    preprocessor_bundle = joblib.load(PREPROCESSOR_PATH)
    preprocessor = preprocessor_bundle["preprocessor"]

    input_row = {}
    for col in numeric_cols + cat_cols:
        input_row[col] = new_user.get(col, np.nan)

    input_df = pd.DataFrame([input_row], dtype=object)

    # هنملأ أي قيم ناقصة بمتوسط/أكثر قيمة تكرارًا من الداتا المرجعية عشان الـ transform ميفشلش
    for col in numeric_cols:
        if pd.isna(input_df.at[0, col]):
            input_df.at[0, col] = reference_df[col].median()
    for col in cat_cols:
        if pd.isna(input_df.at[0, col]) or input_df.at[0, col] is None:
            input_df.at[0, col] = reference_df[col].mode().iloc[0]

    input_transformed = preprocessor.transform(input_df)

    distances, indices = knn.kneighbors(input_transformed, n_neighbors=top_n)

    similar_users = reference_df.iloc[indices[0]].copy()
    similar_users["similarity_distance"] = distances[0]

    display_cols = numeric_cols + cat_cols + [target_col, "similarity_distance"]
    display_cols = [c for c in display_cols if c in similar_users.columns]

    return similar_users[display_cols].reset_index(drop=True)


def main():
    knn, df, target_col = build_similarity_index()

    # مثال تجريبي: بناخد أول صف من الداتا كـ "مستخدم جديد" ونجرب نوصي بيه
    sample_row = df.iloc[0].to_dict()
    print("\n[تجربة] توصيات لمستخدم تجريبي بناءً على أول صف في الداتا:")
    recommendations = recommend_for_user(sample_row, top_n=N_RECOMMENDATIONS)
    print(recommendations)


if __name__ == "__main__":
    main()
