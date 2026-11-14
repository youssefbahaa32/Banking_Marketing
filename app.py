import streamlit as st
import pandas as pd
import joblib
from pathlib import Path

MODEL_PATH = Path(__file__).parent / "bank_model.joblib"

st.set_page_config(page_title="Bank Marketing Predictor", page_icon="🏦", layout="centered")

st.title("🏦 Bank Marketing – Subscription Predictor")
st.write("أدخل بيانات العميل، والتطبيق هيقدّر احتمالية اشتراكه في الخدمة.")

if not MODEL_PATH.exists():
    st.error("ملف bank_model.joblib مش موجود. لازم تشغّل كود التدريب الأول وتحط الملف الناتج بجانب app.py.")
    st.stop()

try:
    saved = joblib.load(MODEL_PATH)
    model = saved["model"]
    threshold_f1 = float(saved["threshold_f1"])
    threshold_profit = float(saved["threshold_profit"])
except Exception as e:
    st.error(f"مش قادر أفتح ملف الموديل. تأكد إنه الملف الناتج من كود التدريب. التفاصيل: {e}")
    st.stop()

st.subheader("بيانات العميل")

c1, c2 = st.columns(2)
with c1:
    age = st.number_input("العمر (age)", min_value=18, max_value=100, value=35)
    balance = st.number_input("رصيد الحساب (balance)", value=1000, step=100)
    day = st.number_input("يوم آخر تواصل في الشهر (day)", min_value=1, max_value=31, value=15)
    campaign = st.number_input("عدد مرات التواصل في الحملة الحالية (campaign)", min_value=1, value=1)
    previous = st.number_input("عدد مرات التواصل السابقة (previous)", min_value=0, value=0)
with c2:
    job = st.selectbox("الوظيفة (job)", ["admin.", "blue-collar", "entrepreneur", "housemaid", "management", "retired", "self-employed", "services", "student", "technician", "unemployed", "unknown"])
    marital = st.selectbox("الحالة الاجتماعية (marital)", ["married", "single", "divorced", "unknown"])
    education = st.selectbox("التعليم (education)", ["primary", "secondary", "tertiary", "unknown"])
    default = st.selectbox("هل عليه تعثر ائتماني؟ (default)", ["no", "yes"])
    housing = st.selectbox("هل لديه قرض سكني؟ (housing)", ["no", "yes"])
    loan = st.selectbox("هل لديه قرض شخصي؟ (loan)", ["no", "yes"])

contact = st.selectbox("وسيلة التواصل (contact)", ["cellular", "telephone", "unknown"])
month = st.selectbox("شهر آخر تواصل (month)", ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"])
poutcome = st.selectbox("نتيجة الحملة السابقة (poutcome)", ["unknown", "failure", "other", "success"])
was_contacted_before = st.radio("هل تم التواصل مع العميل قبل الحملة الحالية؟", ["لا", "نعم"], horizontal=True)

# في بيانات التدريب: pdays = -1 معناها لم يتم التواصل سابقاً،
# ثم الكود يحول -1 إلى 0 ويضيف was_contacted.
if was_contacted_before == "لا":
    pdays = 0
    was_contacted = 0
else:
    pdays = st.number_input("عدد الأيام منذ آخر تواصل (pdays)", min_value=0, max_value=999, value=30)
    was_contacted = 1

st.divider()
st.subheader("إعداد القرار")
threshold_choice = st.radio(
    "اختار طريقة اتخاذ القرار",
    ["أعلى ربح (threshold_profit)", "أفضل F1 (threshold_f1)"],
    horizontal=True
)
threshold = threshold_profit if threshold_choice.startswith("أعلى") else threshold_f1
st.caption(f"الـ threshold المستخدم: {threshold:.3f}")

if st.button("توقّع اشتراك العميل", type="primary", use_container_width=True):
    row = pd.DataFrame([{
        "age": age,
        "job": job,
        "marital": marital,
        "education": education,
        "default": default,
        "balance": balance,
        "housing": housing,
        "loan": loan,
        "contact": contact,
        "day": day,
        "month": month,
        "campaign": campaign,
        "pdays": pdays,
        "previous": previous,
        "poutcome": poutcome,
        "was_contacted": was_contacted,
    }])

    try:
        probability = float(model.predict_proba(row)[0, 1])
        prediction = probability >= threshold
        st.subheader("النتيجة")
        st.metric("احتمالية اشتراك العميل", f"{probability * 100:.1f}%")
        if prediction:
            st.success("التوصية: توقّع أن العميل سيشترك — يُنصح بالتواصل معه.")
        else:
            st.info("التوصية: احتمال الاشتراك أقل من الحد المختار — لا تعطيه أولوية اتصال حالياً.")
        st.caption("ده توقع إحصائي من الموديل، مش ضمان إن العميل هيشترك.")
    except Exception as e:
        st.error(f"حصل خطأ أثناء التوقع: {e}")
        st.write("تأكد إن كل الأعمدة وأنواع البيانات مطابقة لبيانات التدريب.")
