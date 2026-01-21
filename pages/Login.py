import streamlit as st
import mysql.connector

conn = mysql.connector.connect(
            host = "localhost",
            user = "root",
            password = "dbda",
            database = "medguard"
        )

st.title("Login/Sign in")
options = st.selectbox("Login / Sign in: ", ["Login", "Sign in"])
if options == "Login":

    usernamee = st.text_input("Username")
    password = st.text_input("Password", type="password")
    role = st.selectbox("Login as",["Patient", "Doctor"])

    usernamee = usernamee.strip().lower()


    if st.button("Log in"):
        
        cur = conn.cursor()
        if role == "Doctor":


            cur.execute("""
                        select password from doctor_login where username = (%s)
                    """, (usernamee,))
            x  = cur.fetchone()
            if x[0] == password:
                st.session_state.role = role
                st.session_state.logged_in = True
                st.success("Logged in as " + role)
                if role == "Doctor":
                    st.switch_page("pages/Doctor.py")
                else:
                    st.switch_page("pages/Patient.py")
            else:
                st.warning("Incorrect Username or Password ")

        else:
            cur.execute("""
                        select password from patient_login where username = (%s)
                    """, (usernamee,))
            x = cur.fetchone()
            if x[0] == password:
                st.session_state.role = role
                st.session_state.logged_in = True
                st.success("Logged in as " + role)
                if role == "Doctor":
                    st.switch_page("pages/Doctor.py")
                else:
                    st.switch_page("pages/Patient.py")
            else:
                st.warning("User not found")
else:
    role = st.selectbox("Sign in as", ["Patient", "Doctor"])
    name = st.text_input("UserName")
    choose_password = st.text_input("Password", type="password")

    name= name.strip().lower()
    if st.button("Create Account"):

        cur = conn.cursor()
        if role == "Doctor":
            cur.execute("""
                        INSERT INTO doctor_login(username, password)
                        VALUES (%s, %s)
                    """, (name, choose_password))
        else:
            cur.execute("""
                        INSERT INTO patient_login(username, password)
                        VALUES (%s, %s)
                    """, (name, choose_password))

        conn.commit()
        cur.close()
        conn.close()

        st.success("Successfully Created " + role + "'s Account")