# 📊 CryptoDesk Pro — دليل التشغيل الكامل

## متطلبات التشغيل المحلي

```bash
# 1. إنشاء بيئة افتراضية
python -m venv venv
source venv/bin/activate       # Linux/Mac
venv\Scripts\activate          # Windows

# 2. تثبيت المكتبات
pip install -r requirements.txt

# 3. تشغيل التطبيق
streamlit run app.py
```

سيفتح التطبيق تلقائياً على: http://localhost:8501

---

## ☁️ الاستضافة المجانية على Streamlit Cloud

1. ارفع المجلد على GitHub (مستودع عام أو خاص)
2. اذهب إلى: https://share.streamlit.io
3. اضغط "New app" → اختر المستودع → `app.py`
4. اضغط "Deploy" — جاهز خلال دقيقة!

---

## ☁️ الاستضافة على Railway (بديل)

```bash
# تثبيت Railway CLI
npm i -g @railway/cli

# تسجيل الدخول ونشر
railway login
railway init
railway up
```

أضف ملف `Procfile`:
```
web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
```

---

## ملاحظات مهمة

- التطبيق يستخدم Binance **Public API** — لا يحتاج مفتاح API
- جميع الصفقات تجريبية ولا تنفذ أوامر حقيقية
- يُنصح بعدم الاعتماد عليه كنصيحة مالية
