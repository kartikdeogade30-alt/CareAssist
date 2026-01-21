import streamlit as st
from database.db_connection import get_connection

conn = get_connection()

col1, col2 = st.columns([8,2])
with col1:
    st.title("Login/Sign in")
    options = st.selectbox("Login / Sign in: ", ["Login", "Sign in"])

with col2:
    if st.button("Home Page"):
        st.switch_page("pages/Home.py")


if options == "Login":

    usernamee = st.text_input("Username")
    password = st.text_input("Password", type="password")
    role = st.selectbox("Login as",["Patient", "Doctor", "Admin"])

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
                st.warning("Incorrect Username or Password ")

        elif role == "Admin":
            cur.execute("""
                        select password from admin_login where username = (%s)
                    """, (usernamee,))
            x = cur.fetchone()
            if x[0] == password:
                st.session_state.role = role
                st.session_state.logged_in = True
                st.success("Logged in as " + role)
                if role == "Admin":
                    st.switch_page("pages/Admin.py")
            else:
                st.warning("Incorrect Username or Password")

        else:
            cur.execute("""
                            select password from patient_login where username = (%s)
                                """, (usernamee,))
            x = cur.fetchone()
            if x[0] == password:
                st.session_state.role = role
                st.session_state.logged_in = True
                st.success("Logged in as " + role)
                if role == "Admin":
                    st.switch_page("pages/Patient   .py")
            else:
                st.warning("Incorrect Username or Password")
else:
    role = st.selectbox("Sign in as", "Patient")
    name = st.text_input("UserName")
    choose_password = st.text_input("Password", type="password")

    name= name.strip().lower()
    if st.button("Create Account"):

        cur = conn.cursor()
        if role == "Patient":
            cur.execute("""
                        INSERT INTO patient_login(username, password)
                        VALUES (%s, %s)
                    """, (name, choose_password))


        conn.commit()
        cur.close()
        conn.close()

        st.success("Successfully Created " + role + "'s Account")