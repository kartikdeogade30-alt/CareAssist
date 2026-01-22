import streamlit as st
from database.db_connection import get_connection

# --------------------------------------------------
# SAFETY CHECK
# --------------------------------------------------

if (
    "consultation_id" not in st.session_state
    or "patient_id" not in st.session_state
):
    st.error("No active consultation found.")
    st.stop()

consultation_id = st.session_state.consultation_id

st.title("🤖 Consultation Chatbot")
st.caption(f"Consultation ID: {consultation_id}")

# --------------------------------------------------
# INITIALIZE SESSION STATE
# --------------------------------------------------

if "chat_step" not in st.session_state:
    st.session_state.chat_step = 1

if "chat_data" not in st.session_state:
    st.session_state.chat_data = {}

# --------------------------------------------------
# STEP 1 – MAIN COMPLAINT
# --------------------------------------------------

if st.session_state.chat_step == 1:
    st.subheader("Step 1: Describe your main problem")

    complaint = st.text_area("What issue are you facing?")

    if st.button("Next"):
        if not complaint.strip():
            st.warning("Please describe your problem.")
        else:
            st.session_state.chat_data["complaint"] = complaint
            st.session_state.chat_step = 2
            st.rerun()

# --------------------------------------------------
# STEP 2 – SELECT SYMPTOM CATEGORY
# --------------------------------------------------

elif st.session_state.chat_step == 2:
    st.subheader("Step 2: Select symptom category")

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT DISTINCT category
        FROM symptoms_master
        ORDER BY category
    """)
    categories = [row[0] for row in cur.fetchall()]
    cur.close()
    conn.close()

    category = st.selectbox("Choose category", categories)

    if st.button("Next"):
        st.session_state.chat_data["category"] = category
        st.session_state.chat_step = 3
        st.rerun()

# --------------------------------------------------
# STEP 3 – SELECT SYMPTOMS (FILTERED BY CATEGORY)
# --------------------------------------------------

elif st.session_state.chat_step == 3:
    category = st.session_state.chat_data["category"]

    st.subheader(f"Step 3: Select symptoms ({category})")

    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("""
        SELECT symptom_id, symptom_name
        FROM symptoms_master
        WHERE category = %s
        ORDER BY symptom_name
    """, (category,))
    symptoms = cur.fetchall()
    cur.close()
    conn.close()

    symptom_map = {
        s["symptom_name"]: s["symptom_id"] for s in symptoms
    }

    selected = st.multiselect(
        "Select applicable symptoms",
        list(symptom_map.keys())
    )

    if st.button("Next"):
        if not selected:
            st.warning("Please select at least one symptom.")
        else:
            st.session_state.chat_data["symptoms"] = [
                symptom_map[s] for s in selected
            ]
            st.session_state.chat_step = 4
            st.rerun()

# --------------------------------------------------
# STEP 4 – ENTER VITALS
# --------------------------------------------------

elif st.session_state.chat_step == 4:
    st.subheader("Step 4: Enter your vitals")

    height = st.number_input("Height (cm)", min_value=50.0, max_value=250.0)
    weight = st.number_input("Weight (kg)", min_value=10.0, max_value=300.0)
    temperature = st.number_input("Temperature (°C)", min_value=30.0, max_value=45.0)
    systolic = st.number_input("Systolic BP", min_value=50, max_value=250)
    diastolic = st.number_input("Diastolic BP", min_value=30, max_value=150)
    sugar = st.number_input("Blood Sugar", min_value=50, max_value=600)
    heart_rate = st.number_input("Heart Rate", min_value=30, max_value=200)
    spo2 = st.number_input("SpO₂ (%)", min_value=50, max_value=100)

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

# --------------------------------------------------
# STEP 5 – CONFIRM & SUBMIT
# --------------------------------------------------

elif st.session_state.chat_step == 5:
    st.subheader("Step 5: Confirm & Submit")

    st.write("### 📝 Complaint")
    st.write(st.session_state.chat_data["complaint"])

    st.write("### 🗂 Category")
    st.write(st.session_state.chat_data["category"])

    st.write("### 🤒 Symptoms (IDs)")
    st.write(st.session_state.chat_data["symptoms"])

    st.write("### ❤️ Vitals")
    st.json(st.session_state.chat_data["vitals"])

    if st.button("Submit Consultation"):
        conn = get_connection()
        cur = conn.cursor()

        try:
            v = st.session_state.chat_data["vitals"]

            # Insert vitals
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

            # Insert symptoms
            for symptom_id in st.session_state.chat_data["symptoms"]:
                cur.execute("""
                    INSERT INTO consultation_symptoms
                    (consultation_id, symptom_id)
                    VALUES (%s, %s)
                """, (consultation_id, symptom_id))

            conn.commit()

            # Clear session consultation state
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
