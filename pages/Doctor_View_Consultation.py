import streamlit as st
import json
from database.db_connection import get_connection
from services.prediction_service import generate_and_store_prediction
from utils.pdf_report import generate_consultation_pdf

# -------------------------------------------------
# NAVIGATION
# -------------------------------------------------
if st.button("⬅ Back to Doctor Dashboard"):
    st.switch_page("pages/Doctor.py")

# -------------------------------------------------
# AUTH GUARD
# -------------------------------------------------
if (
    "logged_in" not in st.session_state
    or st.session_state.logged_in is not True
    or st.session_state.role != "Doctor"
):
    st.error("Unauthorized access.")
    st.stop()

consultation_id = st.session_state.get("review_consultation_id")
doctor_id = st.session_state.get("doctor_id")

if not consultation_id:
    st.warning("No consultation selected.")
    st.switch_page("pages/Doctor.py")
    st.stop()

st.title("📝 Consultation Details")

# -------------------------------------------------
# DB HELPERS
# -------------------------------------------------
def get_consultation(cid):
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("""
        SELECT
            c.consultation_id,
            c.patient_id,
            c.chief_complaint,
            c.doctor_remarks,
            c.prediction_json,
            c.status,
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
    row = cur.fetchone()
    cur.close()
    conn.close()
    return row


def get_vitals(cid):
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM patient_vitals WHERE consultation_id = %s", (cid,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    return row


def get_symptoms(cid):
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("""
        SELECT sm.symptom_name, sm.category
        FROM consultation_symptoms cs
        JOIN symptoms_master sm ON sm.symptom_id = cs.symptom_id
        WHERE cs.consultation_id = %s
    """, (cid,))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


def submit_review(cid, remarks):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE consultations
        SET doctor_id=%s,
            doctor_remarks=%s,
            status='REVIEWED'
        WHERE consultation_id=%s
    """, (doctor_id, remarks, cid))
    conn.commit()
    cur.close()
    conn.close()

# -------------------------------------------------
# FETCH DATA
# -------------------------------------------------
consultation = get_consultation(consultation_id)
vitals = get_vitals(consultation_id)
symptoms = get_symptoms(consultation_id)
status = consultation["status"]

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
        st.write(f"Height: {vitals['height_cm']} cm")
        st.write(f"Weight: {vitals['weight_kg']} kg")
    with col2:
        st.write(f"Temperature: {vitals['temperature_c']} °F")
        st.write(f"Heart Rate: {vitals['heart_rate']} bpm")
    with col3:
        st.write(f"BP: {vitals['systolic_bp']}/{vitals['diastolic_bp']} mmHg")
        st.write(f"SpO2: {vitals['spO2']} %")
else:
    st.info("Vitals not available.")

# -------------------------------------------------
# AI PREDICTIONS (SAFE, ONE-TIME)
# -------------------------------------------------
st.divider()
st.subheader("🧠 AI Predictions")

# Generate ONLY if missing (original stable behavior)
if not consultation["prediction_json"]:
    st.info("AI prediction not generated yet.")
    generate_and_store_prediction(consultation_id)
    st.rerun()

pred = json.loads(consultation["prediction_json"])

# ---------- VITALS RISK ----------
st.subheader("📈 Vitals Risk Prediction")

if "vitals_risk" in pred:
    vr = pred["vitals_risk"]
    if vr.get("status") == "AVAILABLE":
        st.success(f"Risk Level: {vr.get('risk_level')}")
    else:
        st.warning("Vitals risk not available.")
elif "risk_level" in pred:  # OLD FORMAT
    st.success(f"Risk Level: {pred['risk_level']}")
else:
    st.warning("Vitals risk not available.")

# ---------- DISEASE PREDICTION ----------
st.subheader("🧬 Disease Prediction")

dp = pred.get("disease_prediction")

# NEW FORMAT
if isinstance(dp, dict) and dp.get("status") == "AVAILABLE":
    st.write(f"Primary Disease: {dp.get('primary_disease')}")
    for d in dp.get("predictions", []):
        st.write(f"- {d['disease']} ({d['confidence']*100:.2f}%)")

# OLD FORMAT (NO STATUS KEY)
elif isinstance(dp, dict) and "primary_disease" in dp:
    st.write(f"Primary Disease: {dp.get('primary_disease')}")
    for d in dp.get("predictions", []):
        st.write(f"- {d['disease']} ({d['confidence']*100:.2f}%)")

else:
    st.warning("Disease prediction not available.")

# -------------------------------------------------
# DOCTOR REMARKS
# -------------------------------------------------
st.divider()
st.subheader("🩺 Doctor Remarks")

doctor_remarks = consultation["doctor_remarks"] or ""

if status == "REVIEWED":
    st.write(doctor_remarks if doctor_remarks else "— No remarks added —")
else:
    doctor_remarks = st.text_area(
        "Enter Doctor Remarks",
        value=doctor_remarks,
        height=150
    )

# -------------------------------------------------
# ACTIONS
# -------------------------------------------------
col1, col2 = st.columns(2)

with col1:
    if status == "PENDING":
        if st.button("✅ Submit Review"):
            submit_review(consultation_id, doctor_remarks)
            st.switch_page("pages/Doctor.py")

with col2:
    if status == "REVIEWED":
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
            "risk_prediction": pred,
            "doctor_remarks": consultation["doctor_remarks"],
        })

        st.download_button(
            "⬇ Download PDF",
            pdf,
            file_name=f"consultation_{consultation_id}.pdf"
        )
