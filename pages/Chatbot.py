import streamlit as st
from database.db_connection import get_connection
from services.prediction_service import generate_and_store_prediction
from pages.symptom_extractor import extract_symptoms

# ==================================================
# SAFETY CHECK
# ==================================================
if "consultation_id" not in st.session_state or "patient_id" not in st.session_state:
    st.error("No active consultation found.")
    st.stop()

consultation_id = st.session_state.consultation_id

st.title("🤖 Consultation Chatbot")
st.caption(f"Consultation ID: {consultation_id}")

# ==================================================
# SESSION INITIALIZATION
# ==================================================
if "chat_step" not in st.session_state:
    st.session_state.chat_step = 1

if "chat_data" not in st.session_state:
    st.session_state.chat_data = {}

# ==================================================
# HELPER
# ==================================================
def go_back():
    if st.session_state.chat_step == 5:
        st.session_state.chat_step = 4
    elif st.session_state.chat_step == 4:
        st.session_state.chat_step = 2
    elif st.session_state.chat_step == 2:
        st.session_state.chat_step = 1


# ==================================================
# STEP 1 – CHIEF COMPLAINT
# ==================================================
if st.session_state.chat_step == 1:
    st.subheader("Step 1: Chief Complaint")

    complaint = st.text_area(
        "What issue are you facing?",
        placeholder="e.g. Routine checkup, fever, stomach pain",
        value=st.session_state.chat_data.get("complaint", "")
    )

    if st.button("Next"):
        if not complaint.strip():
            st.warning("Chief complaint is required.")
        else:
            st.session_state.chat_data["complaint"] = complaint
            st.session_state.chat_step = 2
            st.rerun()

# ==================================================
# STEP 2 – SYMPTOMS (OPTIONAL)
# ==================================================
elif st.session_state.chat_step == 2:
    st.subheader("Step 2: Symptoms")

    symptom_text = st.text_area(
        "Describe any symptoms (or type 'no symptoms')",
        placeholder="e.g. fever, cough, headache",
        value=st.session_state.chat_data.get("symptom_text", "")
    )

    col1, col2 = st.columns(2)

    with col1:
        if st.button("⬅ Back"):
            go_back()

    with col2:
        if st.button("Next"):
            if symptom_text.strip().lower() == "no symptoms":
                st.session_state.chat_data["no_symptoms"] = True
                st.session_state.chat_data["symptoms"] = []
            else:
                extracted = extract_symptoms(symptom_text)
                st.session_state.chat_data["symptoms"] = extracted
                st.session_state.chat_data["no_symptoms"] = False

            st.session_state.chat_data["symptom_text"] = symptom_text
            st.session_state.chat_step = 4
            st.rerun()

# ==================================================
# STEP 4 – VITALS (REQUIRED)
# ==================================================
elif st.session_state.chat_step == 4:
    st.subheader("Step 4: Enter Vitals")

    v = st.session_state.chat_data.get("vitals", {})

    height = st.number_input("Height (cm)", 50.0, 250.0, v.get("height", 170.0))
    weight = st.number_input("Weight (kg)", 10.0, 300.0, v.get("weight", 70.0))
    temperature = st.number_input("Temperature (°C)", 30.0, 45.0, v.get("temperature", 37.0))
    systolic = st.number_input("Systolic BP", 50, 250, v.get("systolic", 120))
    diastolic = st.number_input("Diastolic BP", 30, 150, v.get("diastolic", 80))
    sugar = st.number_input("Blood Sugar", 50, 600, v.get("sugar", 100))
    heart_rate = st.number_input("Heart Rate", 30, 200, v.get("heart_rate", 72))
    spo2 = st.number_input("SpO₂ (%)", 50, 100, v.get("spo2", 98))

    col1, col2 = st.columns(2)

    with col1:
        if st.button("⬅ Back"):
            go_back()

    with col2:
        if st.button("Next"):
            st.session_state.chat_data["vitals"] = {
                "height": height,
                "weight": weight,
                "temperature": temperature,
                "systolic": systolic,
                "diastolic": diastolic,
                "sugar": sugar,
                "heart_rate": heart_rate,
                "spo2": spo2,
            }
            st.session_state.chat_step = 5
            st.rerun()

# ==================================================
# STEP 5 – CONFIRM & SUBMIT
# ==================================================
elif st.session_state.chat_step == 5:
    st.subheader("Step 5: Confirm & Submit")

    st.write("### 📝 Chief Complaint")
    st.write(st.session_state.chat_data["complaint"])

    st.write("### 🤒 Symptoms")
    if st.session_state.chat_data.get("no_symptoms"):
        st.info("No symptoms reported.")
    else:
        st.write(st.session_state.chat_data.get("symptoms", []))

    st.write("### ❤️ Vitals")
    st.json(st.session_state.chat_data["vitals"])

    col1, col2 = st.columns(2)

    with col1:
        if st.button("⬅ Back"):
            go_back()

    with col2:
        if st.button("Submit Consultation"):
            conn = get_connection()
            cur = conn.cursor()

            try:
                v = st.session_state.chat_data["vitals"]

                # Update chief complaint
                cur.execute("""
                    UPDATE consultations
                    SET chief_complaint = %s
                    WHERE consultation_id = %s
                """, (st.session_state.chat_data["complaint"], consultation_id))

                # Replace vitals
                cur.execute(
                    "DELETE FROM patient_vitals WHERE consultation_id=%s",
                    (consultation_id,)
                )

                cur.execute("""
                    INSERT INTO patient_vitals
                    (consultation_id, height_cm, weight_kg, temperature_c,
                     systolic_bp, diastolic_bp, blood_sugar,
                     heart_rate, spO2)
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
                """, (
                    consultation_id,
                    v["height"], v["weight"], v["temperature"],
                    v["systolic"], v["diastolic"], v["sugar"],
                    v["heart_rate"], v["spo2"]
                ))

                # Store symptoms (TEXT for now)
                # -----------------------------------------
                # INSERT SYMPTOMS (name → symptom_id)
                # -----------------------------------------

                # clear old symptoms (safe re-submit)
                cur.execute(
                    "DELETE FROM consultation_symptoms WHERE consultation_id = %s",
                    (consultation_id,)
                )

                symptoms = st.session_state.chat_data.get("symptoms", [])

                if symptoms:
                    for symptom_name in symptoms:
                        # fetch symptom_id from master
                        cur.execute("""
                            SELECT symptom_id
                            FROM symptoms_master
                            WHERE symptom_name = %s
                        """, (symptom_name,))
                        
                        row = cur.fetchone()
                        if row:
                            symptom_id = row[0]

                            cur.execute("""
                                INSERT INTO consultation_symptoms
                                (consultation_id, symptom_id)
                                VALUES (%s, %s)
                            """, (consultation_id, symptom_id))


                conn.commit()
                generate_and_store_prediction(consultation_id)

                st.success("Consultation submitted successfully.")
                st.switch_page("pages/Patient.py")

            except Exception as e:
                conn.rollback()
                st.error(f"Submission failed: {e}")

            finally:
                cur.close()
                conn.close()
