import streamlit as st
import json
from database.db_connection import get_connection
from utils.pdf_report import generate_consultation_pdf

# ---- Navigation ----
if st.button("⬅ Back to Patient Dashboard"):
    st.switch_page("pages/Patient.py")

# ---- Guard ----
if "view_consultation_id" not in st.session_state:
    st.stop()

cid = st.session_state.view_consultation_id

# ---- DB Fetch ----
conn = get_connection()
cur = conn.cursor(dictionary=True)

cur.execute("""
    SELECT
        c.consultation_id,
        c.chief_complaint,
        c.doctor_remarks,
        c.prediction_json,
        c.created_at,
        p.full_name AS patient_name,
        p.gender,
        p.date_of_birth,
        d.full_name AS doctor_name
    FROM consultations c
    JOIN patients p ON p.patient_id = c.patient_id
    LEFT JOIN doctors d ON d.doctor_id = c.doctor_id
    WHERE c.consultation_id = %s
""", (cid,))
consultation = cur.fetchone()

cur.execute("SELECT * FROM patient_vitals WHERE consultation_id=%s", (cid,))
vitals = cur.fetchone()

cur.execute("""
    SELECT sm.symptom_name, sm.category
    FROM consultation_symptoms cs
    JOIN symptoms_master sm ON sm.symptom_id = cs.symptom_id
    WHERE cs.consultation_id = %s
""", (cid,))
symptoms = cur.fetchall()

cur.close()
conn.close()

prediction = json.loads(consultation["prediction_json"]) if consultation["prediction_json"] else {}

# ---- UI ----
st.title("📄 Consultation Report")

st.markdown("### 🧑 Patient Details")
st.write(f"**Name:** {consultation['patient_name']}")
st.write(f"**Gender:** {consultation['gender']}")
st.write(f"**Date of Birth:** {consultation['date_of_birth']}")

st.divider()

st.markdown("### 👨‍⚕️ Doctor")
st.write(consultation["doctor_name"] or "— Not Assigned —")

st.divider()

st.markdown("### 📝 Chief Complaint")
st.write(consultation["chief_complaint"])

st.divider()

st.markdown("### ❤️ Vitals")
if vitals:
    col1, col2, col3 = st.columns(3)
    col1.write(f"**Height:** {vitals['height_cm']} cm")
    col1.write(f"**Weight:** {vitals['weight_kg']} kg")

    col2.write(f"**Temperature:** {vitals['temperature_c']} °C")
    col2.write(f"**Heart Rate:** {vitals['heart_rate']} bpm")

    col3.write(f"**Blood Pressure:** {vitals['systolic_bp']}/{vitals['diastolic_bp']} mmHg")
    col3.write(f"**SpO₂:** {vitals['spO2']} %")
else:
    st.info("No vitals recorded.")

st.divider()

st.markdown("### 🤒 Symptoms")
if symptoms:
    for s in symptoms:
        st.write(f"- {s['symptom_name']} ({s['category']})")
else:
    st.write("No symptoms reported.")

st.divider()

st.markdown("### 🤖 AI Prediction")
risk = prediction.get("risk_level", "NOT_AVAILABLE")
st.write(f"**Risk Level:** {risk}")

disease_pred = prediction.get("disease_prediction")
if disease_pred:
    st.write(f"**Primary Disease:** {disease_pred['primary_disease']}")
    st.write("**Top Predictions:**")
    for p in disease_pred["predictions"]:
        st.write(f"- {p['disease']} ({p['confidence']:.2f})")

st.divider()

st.markdown("### 🩺 Doctor Remarks")
st.write(consultation["doctor_remarks"] or "No remarks added.")

# ---- PDF Generation ----
st.divider()

pdf_data = generate_consultation_pdf({
    "patient_name": consultation["patient_name"],
    "gender": consultation["gender"],
    "dob": consultation["date_of_birth"],
    "doctor_name": consultation["doctor_name"],
    "chief_complaint": consultation["chief_complaint"],
    "vitals": {
        "height": vitals["height_cm"] if vitals else None,
        "weight": vitals["weight_kg"] if vitals else None,
        "temperature": vitals["temperature_c"] if vitals else None,
        "bp": f"{vitals['systolic_bp']}/{vitals['diastolic_bp']}" if vitals else None,
        "heart_rate": vitals["heart_rate"] if vitals else None,
        "spo2": vitals["spO2"] if vitals else None,
    },
    "symptoms": [f"{s['symptom_name']} ({s['category']})" for s in symptoms],
    "risk_prediction": risk,
    "doctor_remarks": consultation["doctor_remarks"],
})

st.download_button(
    "⬇ Download Consultation Report (PDF)",
    pdf_data,
    file_name=f"consultation_{cid}.pdf"
)
