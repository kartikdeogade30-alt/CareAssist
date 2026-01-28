import streamlit as st
import hashlib
import datetime
from database.db_connection import get_connection
from utils.audit_logger import log_login_event

# ==================================================
# PASSWORD HASHING
# ==================================================
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


# ==================================================
# PAGE HEADER
# ==================================================
col1, col2 = st.columns([8, 2])
with col1:
    st.title("Login / Sign Up")
with col2:
    if st.button("Home"):
        st.switch_page("pages/Home.py")

option = st.selectbox("Choose action", ["Login", "Sign Up"])

# ==================================================
# SESSION FLAG FOR FORGOT PASSWORD
# ==================================================
if "forgot_password" not in st.session_state:
    st.session_state.forgot_password = False


# ==================================================
# LOGIN SECTION
# ==================================================
if option == "Login" and not st.session_state.forgot_password:

    username = st.text_input("Username").strip().lower()
    password = st.text_input("Password", type="password")
    role = st.selectbox("Login as", ["Patient", "Doctor", "Admin"])

    col1, col2 = st.columns(2)

    # ---------------- LOGIN BUTTON ----------------
    with col1:
        login_clicked = st.button("Log in")

    # ---------------- FORGOT PASSWORD BUTTON ----------------
    with col2:
        if st.button("Forgot Password?"):
            st.session_state.forgot_password = True
            st.rerun()

    if login_clicked:
        conn = get_connection()
        cur = conn.cursor()

        hashed_input_password = hash_password(password)

        # ------------------ PATIENT LOGIN ------------------
        if role == "Patient":
            cur.execute("""
                SELECT user_id, patient_id, password_hash
                FROM patient_login
                WHERE username = %s AND is_active = TRUE
            """, (username,))
            row = cur.fetchone()

            if row and hashed_input_password == row[2]:
                st.session_state.logged_in = True
                st.session_state.role = "Patient"
                st.session_state.patient_id = row[1]

                log_login_event("PATIENT", row[1], "SUCCESS")
                st.switch_page("pages/Patient.py")
            else:
                if row:
                    log_login_event("PATIENT", row[1], "FAILED")
                st.error("Invalid username or password")

        # ------------------ DOCTOR LOGIN ------------------
        elif role == "Doctor":
            cur.execute("""
                SELECT 
                    d.doctor_id,
                    d.full_name,
                    d.specialization,
                    dl.password_hash
                FROM doctor_login dl
                JOIN doctors d ON d.doctor_id = dl.doctor_id_fk
                WHERE dl.username = %s
                  AND dl.is_active = TRUE
                  AND d.is_active = TRUE
            """, (username,))
            row = cur.fetchone()

            if row and hashed_input_password == row[3]:
                st.session_state.logged_in = True
                st.session_state.role = "Doctor"
                st.session_state.doctor_id = row[0]
                st.session_state.doctor_name = row[1]
                st.session_state.doctor_specialization = row[2]

                log_login_event("DOCTOR", row[0], "SUCCESS")
                st.switch_page("pages/Doctor.py")
            else:
                if row:
                    log_login_event("DOCTOR", row[0], "FAILED")
                st.error("Invalid username or password")

        # ------------------ ADMIN LOGIN ------------------
        else:
            cur.execute("""
                SELECT admin_id, password_hash
                FROM admin_login
                WHERE username = %s AND is_active = TRUE
            """, (username,))
            row = cur.fetchone()

            if row and hashed_input_password == row[1]:
                st.session_state.logged_in = True
                st.session_state.role = "Admin"
                st.session_state.admin_id = row[0]

                log_login_event("ADMIN", row[0], "SUCCESS")
                st.switch_page("pages/Admin.py")
            else:
                if row:
                    log_login_event("ADMIN", row[0], "FAILED")
                st.error("Invalid username or password")

        cur.close()
        conn.close()


# ==================================================
# FORGOT PASSWORD FLOW
# ==================================================
elif option == "Login" and st.session_state.forgot_password:

    st.subheader("🔐 Reset Password")

    username = st.text_input("Username").strip().lower()
    role = st.selectbox("Account type", ["Patient", "Doctor", "Admin"])
    new_password = st.text_input("New Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Reset Password"):
            if new_password != confirm_password:
                st.error("Passwords do not match")
                st.stop()

            conn = get_connection()
            cur = conn.cursor()

            hashed = hash_password(new_password)

            if role == "Patient":
                cur.execute("""
                    UPDATE patient_login
                    SET password_hash = %s
                    WHERE username = %s AND is_active = TRUE
                """, (hashed, username))

            elif role == "Doctor":
                cur.execute("""
                    UPDATE doctor_login
                    SET password_hash = %s
                    WHERE username = %s AND is_active = TRUE
                """, (hashed, username))

            else:
                cur.execute("""
                    UPDATE admin_login
                    SET password_hash = %s
                    WHERE username = %s AND is_active = TRUE
                """, (hashed, username))

            if cur.rowcount == 0:
                st.error("User not found or inactive")
                conn.rollback()
            else:
                conn.commit()
                st.success("Password reset successful. Please log in.")
                st.session_state.forgot_password = False

            cur.close()
            conn.close()

    with col2:
        if st.button("⬅ Back to Login"):
            st.session_state.forgot_password = False
            st.rerun()


# ==================================================
# SIGN UP (PATIENT ONLY)
# ==================================================
else:
    st.subheader("Patient Registration")

    full_name = st.text_input("Full Name")
    gender = st.selectbox("Gender", ["MALE", "FEMALE", "OTHER"])
    dob = st.date_input(
        "Date of Birth",
        min_value=datetime.date(1900, 1, 1),
        max_value=datetime.date.today()
    )
    phone = st.text_input("Enter one contact number").strip()
    email = st.text_input("Email")
    username = st.text_input("Choose Username").strip().lower()
    password = st.text_input("Password", type="password")

    if st.button("Create Account"):

        if not phone.isdigit() or len(phone) < 10 or len(phone) > 15:
            st.error("Enter a valid phone number")
            st.stop()

        conn = get_connection()
        cur = conn.cursor()

        cur.execute("SELECT 1 FROM patient_login WHERE username = %s", (username,))
        if cur.fetchone():
            st.error("Username already exists")
        else:
            cur.execute("""
                INSERT INTO patients (full_name, gender, date_of_birth, phone, email)
                VALUES (%s, %s, %s, %s, %s)
            """, (full_name, gender, dob, phone, email))

            patient_id = cur.lastrowid

            cur.execute("""
                INSERT INTO patient_login (patient_id, username, password_hash)
                VALUES (%s, %s, %s)
            """, (patient_id, username, hash_password(password)))

            conn.commit()
            st.success("Account created successfully. Please log in.")

        cur.close()
        conn.close()
