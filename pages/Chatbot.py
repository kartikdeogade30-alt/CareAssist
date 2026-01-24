import streamlit as st
from database.db_connection import get_connection

# ==================================================
# SAFETY CHECK
# ==================================================
# Chatbot must always have an active consultation
# Consultation is created / reused before entering chatbot

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
# chat_step controls the flow
# chat_data temporarily stores all inputs
# IMPORTANT: No DB writes until final submit

if "chat_step" not in st.session_state:
    st.session_state.chat_step = 1

if "chat_data" not in st.session_state:
    st.session_state.chat_data = {}

# ==================================================
# HELPER: BACK NAVIGATION
# ==================================================
def go_back():
    st.session_state.chat_step -= 1
    st.rerun()

# ==================================================
# STEP 1 – CHIEF COMPLAINT (REQUIRED)
# ==================================================
# Always required for clinical context
# Even "Routine checkup" or "No complaints" is valid

if st.session_state.chat_step == 1:
    st.subheader("Step 1: Chief Complaint")

    complaint = st.text_area(
        "What issue are you facing?",
        placeholder="e.g. Routine checkup, Follow-up visit, No specific complaints",
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
# STEP 2 – SYMPTOM CATEGORIES (OPTIONAL)
# ==================================================
# Patient can explicitly say they have NO symptoms
# This avoids forcing incorrect data

elif st.session_state.chat_step == 2:
    st.subheader("Step 2: Symptoms Overview")

    no_symptoms = st.checkbox(
        "I do not have any symptoms",
        value=st.session_state.chat_data.get("no_symptoms", False)
    )

    categories = []
    if not no_symptoms:
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

        selected_categories = st.multiselect(
            "Select symptom categories",
            categories,
            default=st.session_state.chat_data.get("categories", [])
        )
    else:
        selected_categories = []

    col1, col2 = st.columns(2)

    with col1:
        if st.button("⬅ Back"):
            go_back()

    with col2:
        if st.button("Next"):
            if not no_symptoms and not selected_categories:
                st.warning("Select at least one category or choose 'No symptoms'.")
            else:
                st.session_state.chat_data["no_symptoms"] = no_symptoms
                st.session_state.chat_data["categories"] = selected_categories
                st.session_state.chat_step = 3
                st.rerun()

# ==================================================
# STEP 3 – SELECT SYMPTOMS (SKIPPED IF NO SYMPTOMS)
# ==================================================
# If patient has no symptoms, we skip this step entirely

elif st.session_state.chat_step == 3:

    if st.session_state.chat_data.get("no_symptoms"):
        # Explicitly store empty symptoms list
        st.session_state.chat_data["symptoms"] = []
        st.info("No symptoms selected for this consultation.")
        st.session_state.chat_step = 4
        st.rerun()

    st.subheader("Step 3: Select Symptoms")

    categories = st.session_state.chat_data["categories"]

    conn = get_connection()
    cur = conn.cursor(dictionary=True)

    placeholders = ",".join(["%s"] * len(categories))
    query = f"""
        SELECT symptom_id, symptom_name, category
        FROM symptoms_master
        WHERE category IN ({placeholders})
        ORDER BY category, symptom_name
    """
    cur.execute(query, tuple(categories))
    symptoms = cur.fetchall()
    cur.close()
    conn.close()

    # Group symptoms by category for clean UI
    grouped = {}
    for s in symptoms:
        grouped.setdefault(s["category"], []).append(s)

    selected_symptom_ids = []

    for category, items in grouped.items():
        st.markdown(f"**{category}**")
        names = [i["symptom_name"] for i in items]

        chosen = st.multiselect(
            f"Select {category} symptoms",
            names,
            default=[
                i["symptom_name"]
                for i in items
                if i["symptom_id"] in st.session_state.chat_data.get("symptoms", [])
            ],
            key=f"sym_{category}"
        )

        for name in chosen:
            for i in items:
                if i["symptom_name"] == name:
                    selected_symptom_ids.append(i["symptom_id"])

    col1, col2 = st.columns(2)

    with col1:
        if st.button("⬅ Back"):
            go_back()

    with col2:
        if st.button("Next"):
            if not selected_symptom_ids:
                st.warning("Please select at least one symptom.")
            else:
                st.session_state.chat_data["symptoms"] = selected_symptom_ids
                st.session_state.chat_step = 4
                st.rerun()

# ==================================================
# STEP 4 – VITALS (ALWAYS REQUIRED)
# ==================================================
# Vitals represent clinical snapshot
# Exactly ONE vitals row per consultation

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
# STEP 5 – CONFIRM & SUBMIT (SINGLE TRANSACTION)
# ==================================================

elif st.session_state.chat_step == 5:
    st.subheader("Step 5: Confirm & Submit")

    st.write("### 📝 Chief Complaint")
    st.write(st.session_state.chat_data["complaint"])

    if st.session_state.chat_data.get("no_symptoms"):
        st.write("### 🤒 Symptoms")
        st.info("No symptoms reported by patient.")
    else:
        st.write("### 🤒 Symptoms (IDs)")
        st.write(st.session_state.chat_data["symptoms"])

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

                # Save chief complaint
                cur.execute("""
                    UPDATE consultations
                    SET chief_complaint = %s
                    WHERE consultation_id = %s
                """, (
                    st.session_state.chat_data["complaint"],
                    consultation_id
                ))

                # Enforce ONE vitals row per consultation
                cur.execute("""
                    DELETE FROM patient_vitals
                    WHERE consultation_id = %s
                """, (consultation_id,))

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

                # Insert symptoms ONLY if present
                for symptom_id in st.session_state.chat_data.get("symptoms", []):
                    cur.execute("""
                        INSERT INTO consultation_symptoms
                        (consultation_id, symptom_id)
                        VALUES (%s, %s)
                    """, (consultation_id, symptom_id))

                conn.commit()

                # Clear consultation-specific session state
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
