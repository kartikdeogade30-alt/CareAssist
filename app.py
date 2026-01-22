import streamlit as st


# login and role flags
if "role" not in st.session_state:
    st.session_state.role = None

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "submitted" not in st.session_state:
    st.session_state.submitted = False

# ---------- USER IDENTIFIERS ----------
if "patient_id" not in st.session_state:
    st.session_state.patient_id = None

if "doctor_id" not in st.session_state:
    st.session_state.doctor_id = None

if "admin_id" not in st.session_state:
    st.session_state.admin_id = None

st.switch_page("pages/Home.py")


