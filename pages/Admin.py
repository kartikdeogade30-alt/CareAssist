import streamlit as st
from database.db_connection import get_connection
import hashlib

# ==================================================
# SAFETY CHECK
# ==================================================
if st.session_state.get("logged_in") != True or st.session_state.get("role") != "Admin":
    st.warning("Please login as Admin to access this page.")
    st.stop()

st.title("🛡️ Admin Dashboard")
st.caption("System user management & control")

st.divider()

# ==================================================
# HELPER FUNCTION
# ==================================================
def hash_password(password: str) -> str:
    """
    Hash passwords before storing.
    Using SHA256 (kept intentionally).
    """
    return hashlib.sha256(password.encode()).hexdigest()

# ==================================================
# CREATE DOCTOR ACCOUNT + PROFILE
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
        years_of_experience = st.number_input(
            "Years of Experience", min_value=0, step=1
        )
        email = st.text_input("Email")
        phone = st.text_input("Phone")

    submit = st.form_submit_button("Create Doctor")

    if submit:
        if not username or not password or not full_name:
            st.error("Username, password, and full name are required.")
        elif password != confirm_password:
            st.error("Passwords do not match.")
        else:
            conn = get_connection()
            cur = conn.cursor()

            # Check username uniqueness
            cur.execute("""
                SELECT 1 FROM doctor_login WHERE username = %s
            """, (username,))
            if cur.fetchone():
                st.error("Doctor username already exists.")
            else:
                # Insert login
                cur.execute("""
                    INSERT INTO doctor_login (username, password_hash, is_active)
                    VALUES (%s, %s, TRUE)
                """, (username.strip().lower(), hash_password(password)))

                doctor_id = cur.lastrowid

                # Insert profile
                cur.execute("""
                    INSERT INTO doctors (
                        doctor_id, full_name, specialization,
                        license_number, years_of_experience,
                        email, phone
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (
                    doctor_id,
                    full_name,
                    specialization,
                    license_number,
                    years_of_experience,
                    email,
                    phone
                ))

                conn.commit()
                st.success("Doctor account created successfully.")

            cur.close()
            conn.close()

st.divider()

# ==================================================
# VIEW & MANAGE DOCTORS
# ==================================================
st.subheader("👨‍⚕️ Manage Doctor Accounts")

conn = get_connection()
cur = conn.cursor(dictionary=True)

cur.execute("""
    SELECT
        dl.doctor_id,
        dl.username,
        dl.is_active,
        dl.created_at,
        d.full_name,
        d.specialization
    FROM doctor_login dl
    LEFT JOIN doctors d ON d.doctor_id = dl.doctor_id
    ORDER BY dl.created_at DESC
""")

doctors = cur.fetchall()
cur.close()
conn.close()

if not doctors:
    st.info("No doctors found.")
else:
    for doc in doctors:
        col1, col2, col3, col4 = st.columns([4, 3, 2, 2])

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
# SYSTEM OVERVIEW
# ==================================================
st.subheader("📊 System Overview")

conn = get_connection()
cur = conn.cursor()

cur.execute("SELECT COUNT(*) FROM patients")
total_patients = cur.fetchone()[0]

cur.execute("SELECT COUNT(*) FROM consultations")
total_consultations = cur.fetchone()[0]

cur.execute("SELECT COUNT(*) FROM consultations WHERE status = 'PENDING'")
pending_consultations = cur.fetchone()[0]

cur.close()
conn.close()

col1, col2, col3 = st.columns(3)
col1.metric("Total Patients", total_patients)
col2.metric("Total Consultations", total_consultations)
col3.metric("Pending Reviews", pending_consultations)

st.divider()

# ==================================================
# LOGOUT
# ==================================================
if st.button("🚪 Logout"):
    st.session_state.clear()
    st.switch_page("pages/Home.py")
