import streamlit as st
from database.db_connection import get_connection

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
    st.switch_page("Doctor")
    st.stop()

st.title("📝 Consultation Review")

# -------------------------------------------------
# DB FUNCTIONS (MYSQL-CONNECTOR SAFE)
# -------------------------------------------------
def get_consultation(cid):
    conn = get_connection()
    cur = conn.cursor(dictionary=True)

    cur.execute("""
        SELECT
            c.consultation_id,
            c.chief_complaint,
            c.doctor_remarks,
            p.full_name,
            p.gender,
            p.date_of_birth
        FROM consultations c
        JOIN patients p ON p.patient_id = c.patient_id
        WHERE c.consultation_id = %s
    """, (cid,))

    row = cur.fetchone()
    cur.fetchall()  # IMPORTANT: clear result set
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
    cur.fetchall()  # IMPORTANT
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

if not consultation:
    st.error("Consultation not found.")
    st.switch_page("Doctor")
    st.stop()

# -------------------------------------------------
# PATIENT INFO
# -------------------------------------------------
st.subheader("👤 Patient Information")
st.write(f"**Name:** {consultation['full_name']}")
st.write(f"**Gender:** {consultation['gender']}")
st.write(f"**Date of Birth:** {consultation['date_of_birth']}")

st.divider()

# -------------------------------------------------
# CHIEF COMPLAINT
# -------------------------------------------------
st.subheader("📌 Chief Complaint")
st.write(consultation["chief_complaint"] or "No chief complaint provided.")

st.divider()

# -------------------------------------------------
# VITALS
# -------------------------------------------------
st.subheader("🧪 Vitals")

if vitals:
    st.write(f"Height: {vitals['height_cm']} cm")
    st.write(f"Weight: {vitals['weight_kg']} kg")
    st.write(f"Temperature: {vitals['temperature_c']} °C")
    st.write(f"Blood Pressure: {vitals['systolic_bp']}/{vitals['diastolic_bp']}")
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
# DOCTOR REMARKS
# -------------------------------------------------
st.subheader("🩺 Doctor Remarks")

doctor_remarks = st.text_area(
    "Enter diagnosis / notes",
    value=consultation["doctor_remarks"] or "",
    height=180,
    placeholder="Write diagnosis, prescription, and advice here..."
)

# -------------------------------------------------
# ACTION BUTTONS
# -------------------------------------------------
col1, col2 = st.columns(2)

with col1:
    if st.button("✅ Submit Review"):
        if not doctor_remarks.strip():
            st.error("Doctor remarks are mandatory.")
        else:
            submit_review(consultation_id, doctor_remarks)
            st.success("Consultation reviewed successfully.")
            st.session_state.pop("review_consultation_id", None)
            st.switch_page("Doctor")

with col2:
    if st.button("⬅ Go Back"):
        st.session_state.pop("review_consultation_id", None)
        st.switch_page("pages/Doctor.py")
