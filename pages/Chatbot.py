import streamlit as st
from database.db_connection import get_connection
from services.prediction_service import generate_and_store_prediction

# ==================================================
# SAFETY CHECK
# ==================================================
if (
    "consultation_id" not in st.session_state
    or "patient_id" not in st.session_state
):
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
# HELPER FUNCTIONS
# ==================================================
def go_back():
    st.session_state.chat_step -= 1
    st.rerun()


def get_all_symptoms():
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("""
        SELECT symptom_id, symptom_name, category
        FROM symptoms_master
        ORDER BY symptom_name
    """)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


def get_symptom_names_by_ids(symptom_ids):
    if not symptom_ids:
        return []

    conn = get_connection()
    cur = conn.cursor(dictionary=True)

    placeholders = ",".join(["%s"] * len(symptom_ids))
    cur.execute(
        f"""
        SELECT symptom_name, category
        FROM symptoms_master
        WHERE symptom_id IN ({placeholders})
        """,
        tuple(symptom_ids)
    )
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

# ==================================================
# STEP 1 – CHIEF COMPLAINT
# ==================================================
if st.session_state.chat_step == 1:
    st.subheader("Step 1: Chief Complaint")

    complaint = st.text_area(
        "What issue are you facing?",
        placeholder="e.g. Routine checkup, Follow-up visit",
        value=st.session_state.chat_data.get("complaint", "")
    )

    if st.button("Next"):
        if not complaint.strip():
            st.warning("Please enter a brief description.")
        else:
            st.session_state.chat_data["complaint"] = complaint
            st.session_state.chat_step = 2
            st.rerun()

# ==================================================
# STEP 2 – SELECT SYMPTOMS (DIRECT, SEARCHABLE)
# ==================================================
elif st.session_state.chat_step == 2:
    st.subheader("Step 2: Select Symptoms")

    no_symptoms = st.checkbox(
        "I do not have any symptoms",
        value=st.session_state.chat_data.get("no_symptoms", False)
    )

    symptom_ids = []

    if not no_symptoms:
        all_symptoms = get_all_symptoms()

        symptom_map = {
            f"{s['symptom_name']} ({s['category']})": s["symptom_id"]
            for s in all_symptoms
        }

        selected = st.multiselect(
            "Search and select symptoms",
            options=list(symptom_map.keys()),
            default=[
                k for k, v in symptom_map.items()
                if v in st.session_state.chat_data.get("symptoms", [])
            ]
        )

        symptom_ids = [symptom_map[s] for s in selected]

    col1, col2 = st.columns(2)

    with col1:
        if st.button("⬅ Back"):
            go_back()

    with col2:
        if st.button("Next"):
            if not no_symptoms and not symptom_ids:
                st.warning("Select at least one symptom or choose 'No symptoms'.")
            else:
                st.session_state.chat_data["no_symptoms"] = no_symptoms
                st.session_state.chat_data["symptoms"] = symptom_ids
                st.session_state.chat_step = 3
                st.rerun()

# ==================================================
# STEP 3 – VITALS
# ==================================================
elif st.session_state.chat_step == 3:
    st.subheader("Step 3: Enter Vitals")

    v = st.session_state.chat_data.get("vitals", {})

    height = st.number_input("Height (cm)", 50.0, 250.0, v.get("height", 170.0))
    weight = st.number_input("Weight (kg)", 10.0, 300.0, v.get("weight", 70.0))
    temperature = st.number_input("Temperature (°F)", 90.0, 110.0, v.get("temperature", 98.6))
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
            st.session_state.chat_step = 4
            st.rerun()

# ==================================================
# STEP 4 – CONFIRM & SUBMIT
# ==================================================
elif st.session_state.chat_step == 4:
    st.subheader("Step 4: Confirm & Submit")

    st.write("### 📝 Chief Complaint")
    st.write(st.session_state.chat_data["complaint"])

    st.write("### 🤒 Symptoms")
    if st.session_state.chat_data.get("no_symptoms"):
        st.info("No symptoms reported.")
    else:
        symptoms = get_symptom_names_by_ids(
            st.session_state.chat_data.get("symptoms", [])
        )
        for s in symptoms:
            st.write(f"- {s['symptom_name']} ({s['category']})")

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

                # Update complaint
                cur.execute("""
                    UPDATE consultations
                    SET chief_complaint = %s
                    WHERE consultation_id = %s
                """, (st.session_state.chat_data["complaint"], consultation_id))

                # Replace vitals
                cur.execute("DELETE FROM patient_vitals WHERE consultation_id=%s", (consultation_id,))
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

                # 🔥 Replace symptoms
                cur.execute("DELETE FROM consultation_symptoms WHERE consultation_id=%s", (consultation_id,))
                for sid in st.session_state.chat_data.get("symptoms", []):
                    cur.execute("""
                        INSERT INTO consultation_symptoms (consultation_id, symptom_id)
                        VALUES (%s,%s)
                    """, (consultation_id, sid))

                conn.commit()

                generate_and_store_prediction(consultation_id)

                del st.session_state.consultation_id
                del st.session_state.chat_step
                del st.session_state.chat_data

                st.success("Consultation submitted successfully.")
                st.switch_page("pages/Patient.py")

            except Exception as e:
                conn.rollback()
                st.error(f"Submission failed: {e}")

            finally:
                cur.close()
                conn.close()
