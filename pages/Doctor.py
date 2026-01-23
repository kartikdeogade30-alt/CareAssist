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
    st.error("Unauthorized access. Please login as Doctor.")
    st.stop()

doctor_id = st.session_state.doctor_id

# -------------------------------------------------
# DB HELPERS
# -------------------------------------------------
def get_doctor_name(doctor_id):
    conn = get_connection()
    cur = conn.cursor(dictionary=True)

    cur.execute("""
        SELECT username
        FROM doctor_login
        WHERE doctor_id = %s
    """, (doctor_id,))

    row = cur.fetchone()
    cur.close()
    conn.close()

    return row["username"] if row else "Doctor"


def get_pending_consultations():
    conn = get_connection()
    cur = conn.cursor(dictionary=True)

    cur.execute("""
        SELECT
            c.consultation_id,
            c.created_at,
            c.chief_complaint,
            p.full_name
        FROM consultations c
        JOIN patients p ON p.patient_id = c.patient_id
        WHERE c.status = 'PENDING'
        ORDER BY c.created_at ASC
    """)

    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


# -------------------------------------------------
# HEADER (HELLO + LOGOUT)
# -------------------------------------------------
col1, col2 = st.columns([8, 2])

with col1:
    doctor_name = get_doctor_name(doctor_id)
    st.markdown(f"## 👋 Hello Dr. {doctor_name}")

with col2:
    if st.button("🚪 Logout"):
        st.session_state.clear()
        st.switch_page("Login")

st.caption("Pending consultations")
st.divider()

# -------------------------------------------------
# CONSULTATION LIST
# -------------------------------------------------
consultations = get_pending_consultations()

if not consultations:
    st.info("No pending consultations.")
else:
    for row in consultations:
        col1, col2, col3 = st.columns([3, 3, 2])

        # Patient name
        col1.write(f"**{row['full_name']}**")

        # Chief complaint (NULL-safe)
        complaint = row["chief_complaint"] or "No chief complaint provided"
        col2.write(complaint[:80] + ("..." if len(complaint) > 80 else ""))

        # Review button
        if col3.button("Review", key=f"review_{row['consultation_id']}"):
            st.session_state.review_consultation_id = row["consultation_id"]
            st.switch_page("pages/Doctor_View_Consultation.py")
