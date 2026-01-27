import streamlit as st
import json
from database.db_connection import get_connection
from utils.pdf_report import generate_consultation_pdf

# -------------------------------------------------
# AUTH GUARD (DOCTOR ONLY)
# -------------------------------------------------
if (
    "logged_in" not in st.session_state
    or st.session_state.logged_in is not True
    or st.session_state.role != "Doctor"
):
    st.error("Unauthorized access.")
    st.stop()

if "review_consultation_id" not in st.session_state:
    st.warning("No consultation selected.")
    st.switch_page("pages/Doctor.py")
    st.stop()

consultation_id = st.session_state.review_consultation_id
doctor_id = st.session_state.doctor_id

# -------------------------------------------------
# NAVIGATION
# -------------------------------------------------
if st.button("⬅ Back to Doctor Dashboard"):
    st.switch_page("pages/Doctor.py")

st.title("📝 Consultation Details")

# -------------------------------------------------
# DB HELPERS
# -------------------------------------------------
def get_one(q, p):
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute(q, p)
    row = cur.fetchone()
    cur.close()
    conn.close()
    return row


def get_all(q, p):
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute(q, p)
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
    WHERE c.consultation_id=%s
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
    c1, c2, c3 = st.columns(3)
    c1.write(f"Height: {vitals['height_cm']} cm")
    c1.write(f"Weight: {vitals['weight_kg']} kg")
    c2.write(f"Temperature: {vitals['temperature_c']} °F")
    c2.write(f"Heart Rate: {vitals['heart_rate']} bpm")
    c3.write(f"BP: {vitals['systolic_bp']}/{vitals['diastolic_bp']} mmHg")
    c3.write(f"SpO₂: {vitals['spO2']} %")
else:
    st.info("Vitals not available.")

# -------------------------------------------------
# AI PREDICTIONS (DISPLAY ONLY – NO TRIGGERS)
# -------------------------------------------------
st.divider()
st.subheader("🧠 AI Predictions")

if consultation["prediction_json"]:
    pred = json.loads(consultation["prediction_json"])

    st.subheader("📈 Vitals Risk")
    if "vitals_risk" in pred and pred["vitals_risk"].get("status") == "AVAILABLE":
        st.success(pred["vitals_risk"]["risk_level"])
    elif "risk_level" in pred:
        st.success(pred["risk_level"])
    else:
        st.info("Risk not available.")

    st.subheader("🧬 Symptoms Based Condition Suggestion")
    st.text("⚠ AI-generated prediction based on symptoms only.")
    st.text("Not a medical diagnosis")
    dp = pred.get("disease_prediction")
    if isinstance(dp, dict) and "primary_disease" in dp:
        st.write(f"Primary: {dp['primary_disease']}")
        for d in dp.get("predictions", []):
            st.write(f"- {d['disease']} ({d['confidence']*100:.2f}%)")
    else:
        st.info("Disease prediction not available.")
else:
    st.info("AI prediction not available.")

# -------------------------------------------------
# DOCTOR REMARKS
# -------------------------------------------------
st.divider()
st.subheader("🩺 Doctor Remarks")

remarks = consultation["doctor_remarks"] or ""

if status == "REVIEWED":
    st.write(remarks if remarks else "— No remarks added —")
else:
    remarks = st.text_area("Enter Doctor Remarks", value=remarks, height=150)

# -------------------------------------------------
# ACTIONS
# -------------------------------------------------
if status == "PENDING":
    if st.button("✅ Submit Review"):
        submit_review(consultation_id, remarks)
        st.switch_page("pages/Doctor.py")

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
        "risk_prediction": pred if consultation["prediction_json"] else {},
        "doctor_remarks": consultation["doctor_remarks"],
    })

    st.download_button(
        label="⬇ Download PDF",
        data=pdf,  # must be bytes
        file_name=f"consultation_{consultation_id}.pdf",
        mime="application/pdf"
    )

