import streamlit as st


# login and role flags
if "role" not in st.session_state:
    st.session_state.role = None

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "submitted" not in st.session_state:
    st.session_state.submitted = False

st.switch_page("pages/Home.py")


