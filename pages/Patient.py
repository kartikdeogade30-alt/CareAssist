import streamlit as st
from database.db_connection import get_connection
from datetime import timezone
import pytz

IST = pytz.timezone("Asia/Kolkata")

def to_ist(dt):
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(IST)

# --------------------------------------------------
# DB HELPERS
# --------------------------------------------------
def get_patient_info(patient_id):
    conn = get_connection()
    cur = conn.cursor(dictionary=True)

    cur.execute("""
        SELECT full_name, gender, date_of_birth, phone, email
        FROM patients
        WHERE patient_id = %s
    """, (patient_id,))

    row = cur.fetchone()
    cur.close()
    conn.close()
    return row


def get_or_create_pending_consultation(patient_id):
    """
    Reuse existing PENDING consultation if present.
    Otherwise create a new one.
    """
    conn = get_connection()
    cur = conn.cursor()

    # Check for existing pending consultation
    cur.execute("""
        SELECT consultation_id
        FROM consultations
        WHERE patient_id = %s AND status = 'PENDING'
        ORDER BY created_at DESC
        LIMIT 1
    """, (patient_id,))
    row = cur.fetchone()

    if row:
        consultation_id = row[0]

        # 🔥 Clear old data so patient can re-enter
        cur.execute("DELETE FROM patient_vitals WHERE consultation_id=%s", (consultation_id,))
        cur.execute("DELETE FROM consultation_symptoms WHERE consultation_id=%s", (consultation_id,))
        cur.execute("""
            UPDATE consultations
            SET chief_complaint = NULL,
                prediction_json = NULL
            WHERE consultation_id = %s
        """, (consultation_id,))

    else:
        cur.execute("""
            INSERT INTO consultations (patient_id, status)
            VALUES (%s, 'PENDING')
        """, (patient_id,))
        consultation_id = cur.lastrowid

    conn.commit()
    cur.close()
    conn.close()
    return consultation_id


def get_consultation_history(patient_id):
    conn = get_connection()
    cur = conn.cursor(dictionary=True)

    cur.execute("""
        SELECT consultation_id, created_at, status
        FROM consultations
        WHERE patient_id = %s
        ORDER BY created_at DESC
    """, (patient_id,))

    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


# --------------------------------------------------
# PATIENT DASHBOARD
# --------------------------------------------------
def patient_dashboard():
    st.title("🧍 Patient Dashboard")

    if "patient_id" not in st.session_state:
        st.error("Session expired. Please login again.")
        return

    patient_id = st.session_state.patient_id
    patient = get_patient_info(patient_id)

    # -------------------------------
    # PATIENT INFO
    # -------------------------------
    st.subheader("👤 Patient Information")

    col1, col2 = st.columns(2)
    col1.write(f"**Name:** {patient['full_name']}")
    col1.write(f"**Gender:** {patient['gender']}")
    col2.write(f"**DOB:** {patient['date_of_birth']}")
    col2.write(f"**Phone:** {patient['phone']}")

    st.write(f"**Email:** {patient['email']}")
    st.divider()

    # -------------------------------
    # NEW CONSULTATION
    # -------------------------------
    st.subheader("➕ New Consultation")

    if st.button("Start / Continue Consultation"):
        consultation_id = get_or_create_pending_consultation(patient_id)

        st.session_state.consultation_id = consultation_id
        st.session_state.chat_step = 1
        st.session_state.chat_data = {}

        st.switch_page("pages/Chatbot.py")

    st.divider()

    # -------------------------------
    # CONSULTATION HISTORY
    # -------------------------------
    st.subheader("📜 Consultation History")

    history = get_consultation_history(patient_id)

    if not history:
        st.info("No consultations found.")
    else:
        for row in history:
            col1, col2, col3 = st.columns([4, 2, 2])

            ist_time = to_ist(row["created_at"])
            col1.write(ist_time.strftime("%d %b %Y %I:%M %p"))

            col2.write(row["status"])

            if col3.button("View", key=f"view_{row['consultation_id']}"):
                st.session_state.view_consultation_id = row["consultation_id"]
                st.switch_page("pages/View_Consultation.py")


# --------------------------------------------------
# AUTH GUARD
# --------------------------------------------------
if st.session_state.logged_in is not True or st.session_state.role != "Patient":
    st.warning("Please login as Patient.")
    st.stop()
else:
    with st.columns([6, 1, 1])[2]:
        if st.button("Logout"):
            st.session_state.clear()
            st.switch_page("pages/Home.py")

patient_dashboard()
