import streamlit as st
import json
from database.db_connection import get_connection
from services.prediction_service import generate_and_store_prediction
from utils.pdf_report import generate_consultation_pdf

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
            p.full_name,
            p.gender,
            p.date_of_birth
        FROM consultations c
        JOIN patients p ON p.patient_id = c.patient_id
        WHERE c.consultation_id = %s
    """, (cid,))

    row = cur.fetchone()
    cur.close()
    conn.close()
    return row


def get_vitals(cid):
    conn = get_connection()
    cur = conn.cursor(dictionary=True)

    cur.execute("""
        SELECT *
        FROM patient_vitals
        WHERE consultation_id = %s
    """, (cid,))

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
        JOIN symptoms_master sm
            ON sm.symptom_id = cs.symptom_id
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
        SET
            doctor_id = %s,
            doctor_remarks = %s,
            status = 'REVIEWED'
        WHERE consultation_id = %s
          AND status = 'PENDING'
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
# STATUS BANNER
# -------------------------------------------------
if status == "PENDING":
    st.warning("⏳ Consultation pending review")
else:
    st.success("✅ Consultation reviewed (read-only)")

st.divider()

# -------------------------------------------------
# PATIENT INFO
# -------------------------------------------------
st.subheader("👤 Patient Information")
st.write(f"**Name:** {consultation['full_name']}")
st.write(f"**Gender:** {consultation['gender']}")
st.write(f"**DOB:** {consultation['date_of_birth']}")

st.divider()

# -------------------------------------------------
# CHIEF COMPLAINT
# -------------------------------------------------
st.subheader("📌 Chief Complaint")
st.write(consultation["chief_complaint"] or "No complaint provided.")

st.divider()

# -------------------------------------------------
# VITALS
# -------------------------------------------------
st.subheader("🧪 Vitals")

if vitals:
    st.write(f"Height: {vitals['height_cm']} cm")
    st.write(f"Weight: {vitals['weight_kg']} kg")
    st.write(f"Temperature: {vitals['temperature_c']} °C")
    st.write(f"BP: {vitals['systolic_bp']}/{vitals['diastolic_bp']}")
    st.write(f"Heart Rate: {vitals['heart_rate']}")
    st.write(f"SpO₂: {vitals['spO2']}%")
else:
    st.info("No vitals recorded.")

st.divider()

# -------------------------------------------------
# SYMPTOMS
# -------------------------------------------------
st.subheader("🤒 Symptoms")

if symptoms:
    for s in symptoms:
        st.write(f"- {s['symptom_name']} ({s['category']})")
else:
    st.info("No symptoms selected.")

st.divider()

# -------------------------------------------------
# AI RISK PREDICTION (ON DEMAND)
# -------------------------------------------------
st.subheader("🧠 AI Risk Prediction")

if consultation["prediction_json"]:
    prediction = json.loads(consultation["prediction_json"])
    risk = prediction.get("risk_level", "UNKNOWN")

    if risk == "HIGH":
        st.error("🚨 High Risk Patient")
    elif risk == "LOW":
        st.success("✅ Low Risk Patient")
    else:
        st.warning("⚠️ Risk unavailable")
else:
    st.info("AI prediction not generated yet.")
    if status == "PENDING" and st.button("🧠 Generate AI Risk Prediction"):
        with st.spinner("Running AI model..."):
            generate_and_store_prediction(consultation_id)
        st.success("AI prediction generated.")
        st.rerun()

st.divider()

# -------------------------------------------------
# DOCTOR REMARKS
# -------------------------------------------------
st.subheader("🩺 Doctor Remarks")

if status == "REVIEWED":
    st.write(consultation["doctor_remarks"] or "No remarks added.")
else:
    doctor_remarks = st.text_area(
        "Enter diagnosis / notes",
        value=consultation["doctor_remarks"] or "",
        height=160
    )

st.divider()

# -------------------------------------------------
# ACTIONS
# -------------------------------------------------
col1, col2, col3 = st.columns(3)

with col1:
    if status == "PENDING":
        if st.button("✅ Submit Review"):
            if not doctor_remarks.strip():
                st.error("Doctor remarks are mandatory.")
            else:
                submit_review(consultation_id, doctor_remarks)
                st.success("Consultation reviewed.")
                st.session_state.pop("review_consultation_id", None)
                st.switch_page("pages/Doctor.py")

with col2:
    # PDF DOWNLOAD (ONLY AFTER REVIEWED)
    if status == "REVIEWED":
        pdf_bytes = generate_consultation_pdf({
            "consultation_id": consultation_id,
            "patient_name": consultation["full_name"],
            "gender": consultation["gender"],
            "dob": str(consultation["date_of_birth"]),
            "date": consultation["created_at"].strftime("%Y-%m-%d %H:%M"),
            "chief_complaint": consultation["chief_complaint"] or "—",
            "vitals": {
                "height": vitals["height_cm"],
                "weight": vitals["weight_kg"],
                "temperature": vitals["temperature_c"],
                "bp": f"{vitals['systolic_bp']}/{vitals['diastolic_bp']}",
                "heart_rate": vitals["heart_rate"],
                "spo2": vitals["spO2"],
            },
            "symptoms": [
                f"{s['symptom_name']} ({s['category']})"
                for s in symptoms
            ],
            "risk_prediction": (
                json.loads(consultation["prediction_json"]).get("risk_level")
                if consultation["prediction_json"]
                else "Not available"
            ),
            "doctor_remarks": consultation["doctor_remarks"] or "—",
        })

        st.download_button(
            "⬇ Download PDF Report",
            pdf_bytes,
            file_name=f"consultation_{consultation_id}.pdf",
            mime="application/pdf"
        )

with col3:
    if st.button("⬅ Back"):
        st.session_state.pop("review_consultation_id", None)
        st.switch_page("pages/Doctor.py")
