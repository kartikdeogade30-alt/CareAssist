import streamlit as st

st.set_page_config(
    page_title="CareAssist",
    layout="wide",
    initial_sidebar_state="expanded"
)

# login and role flags
if "role" not in st.session_state:
    st.session_state.role = None

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False


# ---------- HEADER ----------
st.title("CareAssist", anchor=False)
st.subheader(
    "Pre-Consultation Health Screening & Decision Support System",
    anchor=False
)

# ---------- INTRO ----------
st.markdown("""
**CareAssist** is a conversational health intake and decision-support platform designed to
assist doctors during **preliminary consultations**.

The system focuses on **structured data collection, validation, and analytics-ready storage**
to support better clinical review — without replacing medical professionals.
""")

# ---------- FEATURES ----------
st.markdown("""
### 🔍 What does CareAssist do?
- Conversational chatbot-based health intake
- Collects patient vitals and reported symptoms
- Validates inputs within medically acceptable ranges
- Generates structured health summaries
- Provides data-driven insights for doctors using analytics tools

### 👥 Who is it for?
- **Patients** – for guided pre-consultation health intake  
- **Doctors** – for reviewing patient data and system-generated summaries  
- **Administrators** – for managing users and system access
""")

# ---------- SAFETY ----------
st.warning(
    "⚠️ Disclaimer: CareAssist provides system-generated summaries and decision support only. "
    "It does not diagnose diseases or prescribe treatment. Final medical decisions must always "
    "be made by qualified healthcare professionals."
)

# ---------- CTA ----------
st.info("Please use the sidebar to log in and continue.")

st.markdown("---")

# ---------- FOOTER ----------
st.markdown("""
📧 **Contact:** elijah031782@gmail.com  
🏫 **Institute:** CDAC ACTS, Pune  
🔗 **GitHub:** https://github.com/kartikdeogade30-alt/CareAssist  
""")
