import streamlit as st
from database.db_connection import get_connection

# DB FUNCTIONS
def get_patient_info(patient_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
    SELECT full_name, gender, date_of_birth, phone, email
    FROM patients
    WHERE patient_id = %s
    """
    cursor.execute(query, (patient_id,))
    patient = cursor.fetchone()

    cursor.close()
    conn.close()
    return patient


def create_new_consultation(patient_id):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO consultations (patient_id)
    VALUES (%s)
    """
    cursor.execute(query, (patient_id,))
    conn.commit()

    consultation_id = cursor.lastrowid

    cursor.close()
    conn.close()
    return consultation_id


def get_consultation_history(patient_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
    SELECT consultation_id, created_at, status
    FROM consultations
    WHERE patient_id = %s
    ORDER BY created_at DESC
    """
    cursor.execute(query, (patient_id,))
    history = cursor.fetchall()

    cursor.close()
    conn.close()
    return history


# --------------------------------------------------
# PATIENT DASHBOARD PAGE
# --------------------------------------------------

def patient_dashboard():
    st.title("🧍 Patient Dashboard")

    # Safety check
    if "patient_id" not in st.session_state:
        st.error("Session expired. Please log in again.")
        return

    patient_id = st.session_state.patient_id

    # -------------------------------
    # PATIENT INFO
    # -------------------------------
    patient = get_patient_info(patient_id)

    st.subheader("👤 Patient Information")

    col1, col2 = st.columns(2)
    col1.write(f"**Name:** {patient['full_name']}")
    col1.write(f"**Gender:** {patient['gender']}")
    col2.write(f"**Date of Birth:** {patient['date_of_birth']}")
    col2.write(f"**Phone:** {patient['phone']}")

    st.write(f"**Email:** {patient['email']}")

    st.divider()


    # START NEW CONSULTATION

    st.subheader("➕ New Consultation")

    if st.button("Start New Consultation"):
        if "consultation_id" not in st.session_state:
            consultation_id = create_new_consultation(patient_id)
            st.session_state.consultation_id = consultation_id
            st.session_state.chat_step = 1
            st.session_state.chat_data = {}

        st.success("New consultation started successfully.")
        st.switch_page("pages/Chatbot.py")

    st.divider()


    # CONSULTATION HISTORY

    st.subheader("📜 Consultation History")

    history = get_consultation_history(patient_id)

    if not history:
        st.info("No consultations found.")
    else:
        for row in history:
            col1, col2, col3 = st.columns([4, 2, 2])

            col1.write(row["created_at"].strftime("%d %b %Y %H:%M"))
            col2.write(row["status"])

            if col3.button(
                "View",
                key=f"view_{row['consultation_id']}"
            ):
                st.session_state.view_consultation_id = row["consultation_id"]
                st.switch_page("pages/View_Consultation.py")


# login and out flags
if st.session_state.logged_in != True or st.session_state.role != "Patient":
    st.warning("Please Login before using this page.")
    st.stop()
else:
    col1, col2, col3 = st.columns([6, 1, 1])
    with col3:
        if st.button("Logout"):
            st.session_state.role = None
            st.session_state.logged_in = False
            st.session_state.submitted = False
            # reset_patient_session()
            st.switch_page("pages/Home.py")

patient_dashboard()