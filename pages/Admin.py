import streamlit as st
from database.db_connection import get_connection
import hashlib
import pandas as pd

# ==================================================
# AUTH GUARD
# ==================================================
if st.session_state.get("logged_in") != True or st.session_state.get("role") != "Admin":
    st.warning("Please login as Admin to access this page.")
    st.stop()

st.title("🛡️ Admin Dashboard")
st.caption("System governance, monitoring & control")

st.divider()

# ==================================================
# HELPERS
# ==================================================
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

# ==================================================
# CREATE DOCTOR ACCOUNT
# ==================================================
st.subheader("➕ Create Doctor Account")

with st.form("create_doctor_form", clear_on_submit=True):
    col1, col2 = st.columns(2)

    with col1:
        username = st.text_input("Doctor Username")
        password = st.text_input("Temporary Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")
        full_name = st.text_input("Full Name")
        specialization = st.text_input("Specialization")

    with col2:
        license_number = st.text_input("License Number")
        years_of_experience = st.number_input("Years of Experience", min_value=0, step=1)
        email = st.text_input("Email")
        phone = st.text_input("Phone")

    submit = st.form_submit_button("Create Doctor")

    if submit:
        if not username or not password or not full_name:
            st.error("Username, password, and full name are required.")
        elif password != confirm_password:
            st.error("Passwords do not match.")
        else:
            uname = username.strip().lower()
            conn = get_connection()
            cur = conn.cursor()

            try:
                cur.execute("SELECT 1 FROM doctor_login WHERE username = %s", (uname,))
                if cur.fetchone():
                    st.error("Doctor username already exists.")
                else:
                    cur.execute("""
                        INSERT INTO doctor_login (username, password_hash, is_active)
                        VALUES (%s, %s, TRUE)
                    """, (uname, hash_password(password)))

                    doctor_id = cur.lastrowid

                    cur.execute("""
                        INSERT INTO doctors (
                            doctor_id, full_name, specialization,
                            license_number, years_of_experience,
                            email, phone
                        )
                        VALUES (%s,%s,%s,%s,%s,%s,%s)
                    """, (
                        doctor_id, full_name, specialization,
                        license_number, years_of_experience,
                        email, phone
                    ))

                    conn.commit()
                    st.success("Doctor account created successfully.")

            except Exception as e:
                conn.rollback()
                st.error(f"Error creating doctor: {e}")
            finally:
                cur.close()
                conn.close()

st.divider()

# ==================================================
# MANAGE DOCTORS
# ==================================================
st.subheader("👨‍⚕️ Doctor Management")

conn = get_connection()
cur = conn.cursor(dictionary=True)

cur.execute("""
    SELECT
        dl.doctor_id,
        dl.username,
        dl.is_active,
        d.full_name,
        d.specialization
    FROM doctor_login dl
    LEFT JOIN doctors d ON d.doctor_id = dl.doctor_id
    ORDER BY dl.created_at DESC
""")
doctors = cur.fetchall()
cur.close()
conn.close()

for doc in doctors:
    col1, col2, col3, col4 = st.columns([4,3,2,2])
    col1.write(f"**{doc['full_name'] or doc['username']}**")
    col2.write(doc["specialization"] or "—")
    col3.write("Active ✅" if doc["is_active"] else "Inactive ❌")

    if col4.button(
        "Deactivate" if doc["is_active"] else "Activate",
        key=f"toggle_{doc['doctor_id']}"
    ):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            UPDATE doctor_login
            SET is_active = NOT is_active
            WHERE doctor_id = %s
        """, (doc["doctor_id"],))
        conn.commit()
        cur.close()
        conn.close()
        st.rerun()

st.divider()

# ==================================================
# DOCTOR ACTIVITY SUMMARY
# ==================================================
st.subheader("📋 Doctor Activity Summary")

conn = get_connection()
df = pd.read_sql("""
    SELECT
        d.full_name AS Doctor,
        COUNT(c.consultation_id) AS Total,
        SUM(c.status = 'PENDING') AS Pending,
        SUM(c.status = 'REVIEWED') AS Reviewed
    FROM doctors d
    LEFT JOIN consultations c ON c.doctor_id = d.doctor_id
    GROUP BY d.doctor_id
""", conn)
conn.close()

st.dataframe(df, use_container_width=True)

st.divider()

# ==================================================
# INACTIVE DOCTOR ALERT
# ==================================================
st.subheader("⚠️ Inactive Doctor Alerts")

conn = get_connection()
cur = conn.cursor()

cur.execute("""
    SELECT COUNT(*)
    FROM consultations c
    JOIN doctor_login dl ON dl.doctor_id = c.doctor_id
    WHERE c.status = 'PENDING' AND dl.is_active = FALSE
""")
inactive_pending = cur.fetchone()[0]
cur.close()
conn.close()

if inactive_pending > 0:
    st.error(f"{inactive_pending} pending consultations assigned to inactive doctors.")
else:
    st.success("No pending consultations with inactive doctors.")

st.divider()

# ==================================================
# RECENT LOGIN ACTIVITY
# ==================================================
st.subheader("🕒 Recent Login Activity")

conn = get_connection()
df_logs = pd.read_sql("""
    SELECT user_type, user_id, login_status, login_time
    FROM login_audit_logs
    ORDER BY login_time DESC
    LIMIT 10
""", conn)
conn.close()

st.dataframe(df_logs, use_container_width=True)

st.divider()

# ==================================================
# PATIENT GROWTH TREND
# ==================================================
st.subheader("📈 Patient Growth")

conn = get_connection()
df_growth = pd.read_sql("""
    SELECT DATE(created_at) AS day, COUNT(*) AS registrations
    FROM patients
    GROUP BY DATE(created_at)
    ORDER BY day
""", conn)
conn.close()

st.line_chart(df_growth.set_index("day"))

st.divider()

# ==================================================
# CONSULTATION BOTTLENECK
# ==================================================
st.subheader("⏱️ Consultation Bottlenecks")

conn = get_connection()
cur = conn.cursor()

cur.execute("""
    SELECT MIN(created_at)
    FROM consultations
    WHERE status = 'PENDING'
""")
oldest_pending = cur.fetchone()[0]

cur.execute("""
    SELECT AVG(TIMESTAMPDIFF(HOUR, created_at, NOW()))
    FROM consultations
    WHERE status = 'PENDING'
""")
avg_pending = cur.fetchone()[0]

cur.close()
conn.close()

col1, col2 = st.columns(2)
col1.metric("Oldest Pending", str(oldest_pending) if oldest_pending else "—")
col2.metric("Avg Pending (hrs)", round(avg_pending, 2) if avg_pending else "—")

st.divider()

# ==================================================
# SYSTEM INFO (READ-ONLY)
# ==================================================
st.subheader("⚙️ System Information")

st.json({
    "Environment": "Streamlit Cloud",
    "Database": "AWS RDS MySQL",
    "ML Model": "Risk Prediction v1",
    "Prediction Mode": "Doctor-triggered"
})

st.divider()

# ==================================================
# LOGOUT
# ==================================================
if st.button("🚪 Logout"):
    st.session_state.clear()
    st.switch_page("pages/Home.py")
