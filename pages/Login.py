import streamlit as st
from database.db_connection import get_connection

# page header
col1, col2 = st.columns([8, 2])
with col1:
    st.title("Login / Sign Up")
with col2:
    if st.button("Home"):
        st.switch_page("pages/Home.py")

option = st.selectbox("Choose action", ["Login", "Sign Up"])

# login

if option == "Login":

    username = st.text_input("Username").strip().lower()
    password = st.text_input("Password", type="password")
    role = st.selectbox("Login as", ["Patient", "Doctor", "Admin"])

    if st.button("Log in"):
        conn = get_connection()
        cur = conn.cursor()

        if role == "Patient":
            cur.execute("""
                SELECT user_id, patient_id, password_hash
                FROM patient_login
                WHERE username = %s AND is_active = TRUE
            """, (username,))
            row = cur.fetchone()

            if row and password == row[2]:
                st.session_state.logged_in = True
                st.session_state.role = "Patient"
                st.session_state.patient_id = row[1]
                st.switch_page("pages/Patient.py")
            else:
                st.error("Invalid username or password")

        elif role == "Doctor":
            cur.execute("""
                SELECT doctor_id, password_hash
                FROM doctor_login
                WHERE username = %s AND is_active = TRUE
            """, (username,))
            row = cur.fetchone()

            if row and password == row[1]:
                st.session_state.logged_in = True
                st.session_state.role = "Doctor"
                st.session_state.doctor_id = row[0]
                st.switch_page("pages/Doctor.py")
            else:
                st.error("Invalid username or password")

        else:  # Admin
            cur.execute("""
                SELECT admin_id, password_hash
                FROM admin_login
                WHERE username = %s AND is_active = TRUE
            """, (username,))
            row = cur.fetchone()

            if row and password == row[1]:
                st.session_state.logged_in = True
                st.session_state.role = "Admin"
                st.session_state.admin_id = row[0]
                st.switch_page("pages/Admin.py")
            else:
                st.error("Invalid username or password")

        cur.close()
        conn.close()

# sign up

else:
    st.subheader("Patient Registration")

    full_name = st.text_input("Full Name")
    gender = st.selectbox("Gender", ["MALE", "FEMALE", "OTHER"])
    dob = st.date_input("Date of Birth")
    phone = st.text_input("Enter one contact number").strip()
    email = st.text_input("Email")
    username = st.text_input("Choose Username").strip().lower()
    password = st.text_input("Password", type="password")

    if st.button("Create Account"):
        if not phone.isdigit()or len(phone) < 10 or len(phone) > 15:
            st.error("Enter valid phone number")
            st.stop()

        conn = get_connection()
        cur = conn.cursor()

        # Check username uniqueness
        cur.execute("""
            SELECT 1 FROM patient_login WHERE username = %s
        """, (username,))
        if cur.fetchone():
            st.error("Username already exists")
        else:
            # Insert patient profile
            cur.execute("""
                INSERT INTO patients (full_name, gender, date_of_birth, phone, email)
                VALUES (%s, %s, %s, %s,%s)
            """, (full_name, gender, dob, phone, email))

            patient_id = cur.lastrowid

            # Insert login credentials
            cur.execute("""
                INSERT INTO patient_login (patient_id, username, password_hash)
                VALUES (%s, %s, %s)
            """, (patient_id, username, password))

            conn.commit()
            st.success("Account created successfully. Please log in.")

        cur.close()
        conn.close()
