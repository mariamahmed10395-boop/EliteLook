# مجلد البيانات

حمّل ملف الداتاست من كاجل من الرابط ده:
https://www.kaggle.com/datasets/zara2099/personalized-clothing-and-body-measurements-data

وحط ملف الـ CSV في المجلد ده بالاسم:

```
raw_data.csv
```

يعني المسار النهائي يكون:
```
pipeline/data/raw_data.csv
```

بعد كده افتح `config.py` في المجلد الرئيسي وعدّل:
- `TARGET_COLUMN`
- `BODY_MEASUREMENT_COLUMNS`
- `CATEGORICAL_COLUMNS`
- `ID_COLUMNS`

عشان تتطابق مع أسماء الأعمدة الفعلية في الملف اللي حمّلته (افتح الملف وشوف أول صف/header).
