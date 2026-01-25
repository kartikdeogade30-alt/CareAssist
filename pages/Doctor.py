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
    cur.fetchall()
    cur.close()
    conn.close()

    return row["username"] if row else "Doctor"


def get_consultations_by_status(status):
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
        WHERE c.status = %s
        ORDER BY c.created_at DESC
    """, (status,))

    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


# -------------------------------------------------
# HEADER
# -------------------------------------------------
col1, col2 = st.columns([8, 2])

with col1:
    doctor_name = get_doctor_name(doctor_id)
    st.markdown(f"## 👋 Hello Dr. {doctor_name}")

with col2:
    if st.button("🚪 Logout"):
        st.session_state.clear()
        st.switch_page("pages/Login.py")

st.divider()

# -------------------------------------------------
# SEARCH
# -------------------------------------------------
search_query = st.text_input(
    "🔍 Search patient by name",
    placeholder="Type patient name..."
).strip().lower()

# -------------------------------------------------
# PENDING CONSULTATIONS
# -------------------------------------------------
st.subheader("🔴 Pending Consultations")

pending_consultations = get_consultations_by_status("PENDING")

if search_query:
    pending_consultations = [
        c for c in pending_consultations
        if search_query in c["full_name"].lower()
    ]

if not pending_consultations:
    st.info("No pending consultations found.")
else:
    for row in pending_consultations:
        col1, col2, col3 = st.columns([3, 4, 2])

        col1.write(f"**{row['full_name']}**")

        complaint = row["chief_complaint"] or "No chief complaint provided"
        col2.write(complaint[:90] + ("..." if len(complaint) > 90 else ""))

        if col3.button("Review", key=f"review_{row['consultation_id']}"):
            st.session_state.review_consultation_id = row["consultation_id"]
            st.switch_page("pages/Doctor_View_Consultation.py")

st.divider()

# -------------------------------------------------
# REVIEWED CONSULTATIONS (VIEW ONLY)
# -------------------------------------------------
st.subheader("✅ Patients Already Served")

reviewed_consultations = get_consultations_by_status("REVIEWED")

if search_query:
    reviewed_consultations = [
        c for c in reviewed_consultations
        if search_query in c["full_name"].lower()
    ]

if not reviewed_consultations:
    st.info("No reviewed consultations yet.")
else:
    for row in reviewed_consultations:
        col1, col2, col3 = st.columns([3, 4, 2])

        col1.write(f"**{row['full_name']}**")

        complaint = row["chief_complaint"] or "No chief complaint provided"
        col2.write(complaint[:90] + ("..." if len(complaint) > 90 else ""))

        if col3.button("View", key=f"view_{row['consultation_id']}"):
            st.session_state.review_consultation_id = row["consultation_id"]
            st.session_state.view_only = True
            st.switch_page("pages/Doctor_View_Consultation.py")
