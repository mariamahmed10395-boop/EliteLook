# -*- coding: utf-8 -*-
"""
config.py
=========
إعدادات مشتركة لكل ملفات الـ pipeline (المسارات + أسماء الأعمدة).

عدّل القيم هنا فقط بدل ما تعدّل كل ملف لوحده.
الداتاست المستهدف:
https://www.kaggle.com/datasets/zara2099/personalized-clothing-and-body-measurements-data

حمّل ملف الـ CSV من كاجل وحطه هنا:
    pipeline/data/raw_data.csv
"""

import os

# ---------------------------------------------------------------------------
# المسارات (Paths)
# ---------------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_DIR = os.path.join(BASE_DIR, "data")
RAW_DATA_PATH = os.path.join(DATA_DIR, "raw_data.csv")

OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")
PROCESSED_DIR = os.path.join(OUTPUT_DIR, "processed")
MODELS_DIR = os.path.join(OUTPUT_DIR, "models")
REPORTS_DIR = os.path.join(OUTPUT_DIR, "reports")

LOADED_DATA_PATH = os.path.join(PROCESSED_DIR, "01_loaded_data.pkl")
CLEANED_DATA_PATH = os.path.join(PROCESSED_DIR, "02_cleaned_data.pkl")
FEATURED_DATA_PATH = os.path.join(PROCESSED_DIR, "03_featured_data.pkl")
PREPROCESSOR_PATH = os.path.join(MODELS_DIR, "preprocessor.pkl")

TRAIN_TEST_SPLIT_PATH = os.path.join(PROCESSED_DIR, "04_train_test_split.pkl")
BASELINE_MODEL_PATH = os.path.join(MODELS_DIR, "baseline_model.pkl")
TUNED_MODEL_PATH = os.path.join(MODELS_DIR, "tuned_model.pkl")
FINAL_MODEL_PATH = os.path.join(MODELS_DIR, "final_model.pkl")

EVALUATION_REPORT_PATH = os.path.join(REPORTS_DIR, "evaluation_report.json")
SIMILARITY_INDEX_PATH = os.path.join(MODELS_DIR, "similarity_index.pkl")

for _d in (DATA_DIR, PROCESSED_DIR, MODELS_DIR, REPORTS_DIR):
    os.makedirs(_d, exist_ok=True)

# ---------------------------------------------------------------------------
# أعمدة الداتاست (عدّلها لو أسماء الأعمدة عندك مختلفة شوية بعد ما تفتح الـ CSV)
# ---------------------------------------------------------------------------

# عمود الهدف (target) اللي هنتنبأ بيه: مقاس/فيت مناسب (Recommended Size / Fit)
TARGET_COLUMN = "recommended_size"

# أعمدة القياسات الجسدية (numeric)
BODY_MEASUREMENT_COLUMNS = [
    "height",
    "weight",
    "chest",
    "waist",
    "hips",
    "shoulder_width",
    "arm_length",
    "leg_length",
    "age",
]

# أعمدة تصنيفية (categorical) زي الجنس، تفضيلات القماش، نوع الملابس، إلخ
CATEGORICAL_COLUMNS = [
    "gender",
    "body_shape",
    "fit_preference",
    "fabric_preference",
    "occasion",
    "clothing_category",
]

# أعمدة نصية/معرفات مش هتدخل في التدريب (تتشال في الـ preprocessing)
ID_COLUMNS = [
    "user_id",
    "customer_id",
]

# نسبة بيانات الاختبار
TEST_SIZE = 0.2
RANDOM_STATE = 42

# عدد الجيران المستخدمين في محرك التوصية (KNN)
N_RECOMMENDATIONS = 5
