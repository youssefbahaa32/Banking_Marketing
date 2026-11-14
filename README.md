# Bank Marketing Deployment

## محتويات المشروع
- `app.py`: واجهة التطبيق التي يدخل منها المستخدم بيانات العميل.
- `requirements.txt`: المكتبات المطلوبة لتشغيل التطبيق.
- `bank_model.joblib`: ملف الموديل الناتج من كود التدريب (يجب إضافته بنفسك).

## قبل التشغيل
1. شغّل كود التدريب الأصلي في نفس مجلد ملف البيانات `bank_marketing.csv`.
2. بعد انتهاء التدريب، سيُنشئ الكود ملف `bank_model.joblib`.
3. انسخ `bank_model.joblib` إلى نفس مجلد `app.py`.

## تشغيل التطبيق على جهازك
افتح Terminal داخل المجلد، ثم نفّذ:

```bash
pip install -r requirements.txt
streamlit run app.py
```

سيفتح التطبيق في المتصفح.

## النشر على Streamlit Community Cloud
1. ارفع `app.py` و`requirements.txt` و`bank_model.joblib` إلى GitHub repository.
2. افتح https://share.streamlit.io/
3. اختر المستودع، وحدد `app.py` كملف التشغيل، ثم Deploy.

> ملاحظة: لا ترفع بيانات عملاء حقيقية أو معلومات شخصية حساسة إلى مستودع عام. استخدم بيانات تجريبية، واجعل المستودع Private إذا كان يحتوي على ملفات غير عامة.
