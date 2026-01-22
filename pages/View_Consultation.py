import streamlit as st
from database.db_connection import get_connection

# --------------------------------------------------
# SAFETY CHECK
# --------------------------------------------------

if "view_consultation_id" not in st.session_state:
    st.error("No consultation selected.")
    st.stop()

consultation_id = st.session_state.view_consultation_id

st.title("📄 Consultation Details")
st.caption(f"Consultation ID: {consultation_id}")

conn = get_connection()

# --------------------------------------------------
# FETCH VITALS (USE fetchall)
# --------------------------------------------------

cur1 = conn.cursor(dictionary=True)
cur1.execute("""
    SELECT *
    FROM patient_vitals
    WHERE consultation_id = %s
""", (consultation_id,))

vitals_rows = cur1.fetchall()   # ✅ consume everything
cur1.close()

vitals = vitals_rows[0] if vitals_rows else None

# --------------------------------------------------
# FETCH SYMPTOMS
# --------------------------------------------------

cur2 = conn.cursor(dictionary=True)
cur2.execute("""
    SELECT sm.symptom_name, sm.category
    FROM consultation_symptoms cs
    JOIN symptoms_master sm
        ON cs.symptom_id = sm.symptom_id
    WHERE cs.consultation_id = %s
""", (consultation_id,))

symptoms = cur2.fetchall()
cur2.close()

conn.close()

# --------------------------------------------------
# DISPLAY
# --------------------------------------------------

st.subheader("🤒 Symptoms")
if symptoms:
    for s in symptoms:
        st.write(f"- {s['symptom_name']} ({s['category']})")
else:
    st.info("No symptoms recorded.")

st.subheader("❤️ Vitals")
if vitals:
    st.json({
        "Height (cm)": vitals["height_cm"],
        "Weight (kg)": vitals["weight_kg"],
        "Temperature (°C)": vitals["temperature_c"],
        "Blood Pressure": f"{vitals['systolic_bp']}/{vitals['diastolic_bp']}",
        "Blood Sugar": vitals["blood_sugar"],
        "Heart Rate": vitals["heart_rate"],
        "SpO2": vitals["spO2"]
    })
else:
    st.info("No vitals recorded.")

st.divider()

if st.button("⬅ Back to Dashboard"):
    del st.session_state.view_consultation_id
    st.switch_page("pages/Patient.py")
