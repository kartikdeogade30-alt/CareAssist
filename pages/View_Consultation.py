import streamlit as st
import json
from database.db_connection import get_connection
from utils.pdf_report import generate_consultation_pdf

# -------------------------------------------------
# NAVIGATION
# -------------------------------------------------
if st.button("⬅ Back to Patient Dashboard"):
    st.switch_page("pages/Patient.py")

# -------------------------------------------------
# AUTH GUARD
# -------------------------------------------------
if (
    "logged_in" not in st.session_state
    or st.session_state.logged_in is not True
    or st.session_state.role != "Patient"
):
    st.error("Unauthorized access.")
    st.stop()

consultation_id = st.session_state.get("view_consultation_id")

if not consultation_id:
    st.warning("No consultation selected.")
    st.switch_page("pages/Patient.py")
    st.stop()

st.title("📄 Consultation Report")

# -------------------------------------------------
# DB HELPERS
# -------------------------------------------------
def get_one(query, params):
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute(query, params)
    row = cur.fetchone()
    cur.close()
    conn.close()
    return row


def get_all(query, params):
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute(query, params)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


# -------------------------------------------------
# FETCH DATA
# -------------------------------------------------
consultation = get_one("""
    SELECT
        c.consultation_id,
        c.chief_complaint,
        c.doctor_remarks,
        c.prediction_json,
        c.status,
        p.full_name AS patient_name,
        p.gender,
        p.date_of_birth,
        d.full_name AS doctor_name
    FROM consultations c
    JOIN patients p ON p.patient_id = c.patient_id
    LEFT JOIN doctors d ON d.doctor_id = c.doctor_id
    WHERE c.consultation_id = %s
""", (consultation_id,))

vitals = get_one(
    "SELECT * FROM patient_vitals WHERE consultation_id=%s",
    (consultation_id,)
)

symptoms = get_all("""
    SELECT sm.symptom_name, sm.category
    FROM consultation_symptoms cs
    JOIN symptoms_master sm ON sm.symptom_id = cs.symptom_id
    WHERE cs.consultation_id=%s
""", (consultation_id,))

# -------------------------------------------------
# BASIC INFO
# -------------------------------------------------
st.subheader("👤 Patient Information")
st.write(f"Name: {consultation['patient_name']}")
st.write(f"Gender: {consultation['gender']}")
st.write(f"DOB: {consultation['date_of_birth']}")

st.divider()

st.subheader("📌 Chief Complaint")
st.write(consultation["chief_complaint"])

# -------------------------------------------------
# SYMPTOMS
# -------------------------------------------------
st.divider()
st.subheader("😷 Symptoms")

if symptoms:
    for s in symptoms:
        st.write(f"- {s['symptom_name']} ({s['category']})")
else:
    st.info("No symptoms reported.")

# -------------------------------------------------
# VITALS
# -------------------------------------------------
st.divider()
st.subheader("❤️ Vitals")

if vitals:
    col1, col2, col3 = st.columns(3)

    with col1:
        st.write(f"**Height:** {vitals['height_cm']} cm")
        st.write(f"**Weight:** {vitals['weight_kg']} kg")

    with col2:
        st.write(f"**Temperature:** {vitals['temperature_c']} °F")
        st.write(f"**Heart Rate:** {vitals['heart_rate']} bpm")

    with col3:
        st.write(f"**Blood Pressure:** {vitals['systolic_bp']}/{vitals['diastolic_bp']} mmHg")
        st.write(f"**SpO₂:** {vitals['spO2']} %")
else:
    st.info("Vitals not available.")

# -------------------------------------------------
# AI PREDICTIONS (STRICTLY AFTER REVIEW)
# -------------------------------------------------
st.divider()
st.subheader("🤖 AI Insights")

if consultation["status"] != "REVIEWED":
    st.info("AI insights will be available after doctor review.")
else:
    prediction = json.loads(consultation["prediction_json"]) if consultation["prediction_json"] else {}

    # ---- Vitals Risk ----
    st.subheader("📈 Health Risk")

    vr = prediction.get("vitals_risk", {})
    if vr.get("status") == "AVAILABLE":
        st.write(f"Risk Level: **{vr['risk_level']}**")
    else:
        st.info("Risk assessment not available.")

    # ---- Disease Prediction ----
    st.subheader("🧬 Possible Conditions")

    dp = prediction.get("disease_prediction", {})
    if dp.get("status") == "AVAILABLE":
        st.write(f"**Primary Condition:** {dp['primary_disease']}")
        for d in dp.get("predictions", []):
            st.write(f"- {d['disease']} ({d['confidence']*100:.2f}%)")
    else:
        st.info("Disease prediction not available.")

# -------------------------------------------------
# DOCTOR REMARKS
# -------------------------------------------------
st.divider()
st.subheader("🩺 Doctor Remarks")

if consultation["status"] == "REVIEWED":
    st.write(consultation["doctor_remarks"] or "— No remarks added —")
else:
    st.info("Doctor remarks will be available after review.")

# -------------------------------------------------
# PDF DOWNLOAD (ONLY AFTER REVIEW)
# -------------------------------------------------
st.divider()

if consultation["status"] == "REVIEWED":
    pdf = generate_consultation_pdf({
        "patient_name": consultation["patient_name"],
        "gender": consultation["gender"],
        "dob": consultation["date_of_birth"],
        "doctor_name": consultation["doctor_name"],
        "chief_complaint": consultation["chief_complaint"],
        "vitals": {
            "height": vitals["height_cm"] if vitals else None,
            "weight": vitals["weight_kg"] if vitals else None,
            "temperature": f"{vitals['temperature_c']} °F" if vitals else None,
            "bp": f"{vitals['systolic_bp']}/{vitals['diastolic_bp']}" if vitals else None,
            "heart_rate": vitals["heart_rate"] if vitals else None,
            "spo2": vitals["spO2"] if vitals else None,
        },
        "symptoms": [f"{s['symptom_name']} ({s['category']})" for s in symptoms],
        "risk_prediction": prediction,
        "doctor_remarks": consultation["doctor_remarks"],
    })

    st.download_button(
        "⬇ Download Consultation Report (PDF)",
        pdf,
        file_name=f"consultation_{consultation_id}.pdf"
    )
else:
    st.info("PDF will be available after doctor review.")
