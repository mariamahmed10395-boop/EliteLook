# Pipeline: نظام توصية بالمقاس/الفيت المناسب للملابس
### (Personalized Clothing & Body Measurements Recommendation Pipeline)

مبني على الداتاست:
https://www.kaggle.com/datasets/zara2099/personalized-clothing-and-body-measurements-data

---

## 1. التجهيز (Setup)

```bash
cd pipeline
python -m venv venv
source venv/bin/activate      # على ويندوز: venv\Scripts\activate
pip install -r requirements.txt
```

## 2. تحميل الداتا

- حمّل ملف الـ CSV من كاجل.
- حطه في: `data/raw_data.csv`
- افتح `config.py` وعدّل أسماء الأعمدة (`TARGET_COLUMN`, `BODY_MEASUREMENT_COLUMNS`,
  `CATEGORICAL_COLUMNS`, `ID_COLUMNS`) بحيث تطابق الأعمدة الحقيقية الموجودة
  في الملف اللي حمّلته (افتح الـ CSV وشوف الـ header بتاعه).

## 3. هيكل المشروع

```
pipeline/
│
├── config.py                     # كل الإعدادات والمسارات وأسماء الأعمدة
├── requirements.txt
├── run_all.py                    # تشغيل كل الخطوات دفعة واحدة (ما عدا التوليف)
│
├── data/
│   └── raw_data.csv              # (تحطه إنت) ملف الداتاست الخام من كاجل
│
├── outputs/
│   ├── processed/                # الداتا بعد كل مرحلة (pickle)
│   ├── models/                   # الـ preprocessor + الموديلات المتدربة
│   └── reports/                  # تقرير التقييم (JSON)
│
├── 01_data_loading.py            # تحميل الداتا + فحص أولي
├── 02_data_preprocessing.py      # تنظيف: نواقص، تكرار، شواذ
├── 03_feature_engineering.py     # فيتشرز جديدة (BMI, نسب الجسم) + ترميز/تحجيم
├── 04_model_training.py          # تدريب موديل أساسي (RandomForest)
├── 05_model_tuning.py            # ضبط الـ hyperparameters (RandomizedSearchCV)
├── 06_model_evaluation.py        # تقييم شامل + تقرير JSON
├── 07_recommendation_engine.py   # محرك توصية بالتشابه (KNN)
└── 08_inference.py               # نقطة الاستخدام النهائية (توقع + توصية)
```

## 4. طريقة التشغيل

### تشغيل كل الخطوات دفعة واحدة (بدون التوليف):
```bash
python run_all.py
```

### أو خطوة بخطوة (الترتيب مهم):
```bash
python 01_data_loading.py
python 02_data_preprocessing.py
python 03_feature_engineering.py
python 04_model_training.py
python 05_model_tuning.py        # اختياري - بياخد وقت أطول
python 06_model_evaluation.py
python 07_recommendation_engine.py
python 08_inference.py
```

## 5. إزاي تستخدم النظام على مستخدم جديد

في `08_inference.py` فيه دالة جاهزة:

```python
from importlib import import_module
inference = import_module("08_inference")

result = inference.predict_for_user({
    "height": 170,
    "weight": 65,
    "chest": 90,
    "waist": 75,
    "hips": 95,
    "gender": "female",
    "fit_preference": "regular",
})

print(result["predicted_size"])       # المقاس المتوقع
print(result["similar_users"])        # أقرب مستخدمين شبهه
```

## 6. ملاحظات مهمة

- كل ملف بيقرا مخرجات الملف اللي قبله من مجلد `outputs/` — يعني لازم تشغّلهم بالترتيب
  أول مرة.
- لو أسماء الأعمدة في الداتاست اللي حمّلته مختلفة عن اللي مكتوبة في `config.py`،
  الكود فيه "اكتشاف تلقائي" بيحاول يتعامل مع الموقف، بس الأفضل إنك تظبط
  `config.py` بنفسك من أول مرة عشان نتايج أدق.
- الموديل الأساسي المستخدم هو `RandomForestClassifier`، وسهل تستبدله بأي
  موديل تاني من scikit-learn في `04_model_training.py` و `05_model_tuning.py`.
