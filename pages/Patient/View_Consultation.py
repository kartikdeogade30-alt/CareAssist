import streamlit as st
from database.db_connection import get_connection

# ==================================================
# SAFETY CHECK
# ==================================================
# This page must be opened only after selecting a consultation

if "view_consultation_id" not in st.session_state:
    st.error("No consultation selected.")
    st.stop()

consultation_id = st.session_state.view_consultation_id

st.title("📄 Consultation Details")
st.caption(f"Consultation ID: {consultation_id}")

# ==================================================
# DATABASE CONNECTION
# ==================================================

conn = get_connection()

# ==================================================
# FETCH CONSULTATION-LEVEL DETAILS
# ==================================================
# Consultation table holds contextual information:
# - chief complaint
# - doctor remarks
# - status

cur0 = conn.cursor(dictionary=True)
cur0.execute("""
    SELECT
        consultation_id,
        chief_complaint,
        doctor_remarks,
        status,
        created_at
    FROM consultations
    WHERE consultation_id = %s
""", (consultation_id,))
consultation = cur0.fetchone()
cur0.close()

# ==================================================
# FETCH VITALS (ONE ROW PER CONSULTATION)
# ==================================================
# By design: exactly one vitals snapshot per consultation

cur1 = conn.cursor(dictionary=True)
cur1.execute("""
    SELECT *
    FROM patient_vitals
    WHERE consultation_id = %s
""", (consultation_id,))
vitals_rows = cur1.fetchall()
cur1.close()

vitals = vitals_rows[0] if vitals_rows else None

# ==================================================
# FETCH SYMPTOMS (MAY BE ZERO ROWS)
# ==================================================
# Zero rows is a VALID state (patient explicitly reported no symptoms)

cur2 = conn.cursor(dictionary=True)
cur2.execute("""
    SELECT
        sm.symptom_name,
        sm.category
    FROM consultation_symptoms cs
    JOIN symptoms_master sm
        ON cs.symptom_id = sm.symptom_id
    WHERE cs.consultation_id = %s
    ORDER BY sm.category, sm.symptom_name
""", (consultation_id,))
symptoms = cur2.fetchall()
cur2.close()

conn.close()

# ==================================================
# DISPLAY: CHIEF COMPLAINT
# ==================================================

st.subheader("📝 Chief Complaint")

if consultation and consultation.get("chief_complaint"):
    st.write(consultation["chief_complaint"])
else:
    st.info("No chief complaint recorded.")

st.divider()

# ==================================================
# DISPLAY: SYMPTOMS (NO-SYMPTOMS AWARE)
# ==================================================
# Important UX distinction:
# - No rows ≠ missing data
# - No rows = patient reported no symptoms

st.subheader("🤒 Symptoms")

if symptoms:
    for s in symptoms:
        st.write(f"- {s['symptom_name']} ({s['category']})")
else:
    st.info("Patient reported no symptoms for this consultation.")

st.divider()

# ==================================================
# DISPLAY: VITALS (FORMATTED)
# ==================================================
# DECIMAL values converted to float for clean UI

st.subheader("❤️ Vitals")

if vitals:
    st.json({
        "Height (cm)": float(vitals["height_cm"]) if vitals["height_cm"] else None,
        "Weight (kg)": float(vitals["weight_kg"]) if vitals["weight_kg"] else None,
        "Temperature (°C)": float(vitals["temperature_c"]) if vitals["temperature_c"] else None,
        "Blood Pressure": f"{vitals['systolic_bp']}/{vitals['diastolic_bp']}",
        "Blood Sugar": vitals["blood_sugar"],
        "Heart Rate": vitals["heart_rate"],
        "SpO₂": vitals["spO2"]
    })
else:
    st.info("No vitals recorded.")

st.divider()

# ==================================================
# DISPLAY: DOCTOR REMARKS (READ-ONLY FOR NOW)
# ==================================================

st.subheader("🩺 Doctor Remarks")

if consultation and consultation.get("doctor_remarks"):
    st.write(consultation["doctor_remarks"])
else:
    st.info("Doctor has not added remarks yet.")

st.divider()

# ==================================================
# NAVIGATION
# ==================================================

if st.button("⬅ Back to Dashboard"):
    del st.session_state.view_consultation_id
    st.switch_page("pages/Patient.py")
