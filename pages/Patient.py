import streamlit as st
import streamlit.components.v1 as components
import mysql.connector

if "submitted" not in st.session_state:
    st.session_state.submitted = False

if st.session_state.logged_in != True or st.session_state.role != "Patient":
    st.warning("Please Login before using this page.")
    st.stop()
else:
    col1, col2, col3 = st.columns([6, 1, 1])
    with col3:
        if st.button("Logout"):
            st.session_state.role = None
            st.session_state.logged_in = False
            st.session_state.submitted = False
            st.switch_page("pages/Home.py")


    with col1:
        st.title("Hello Patient")


if st.session_state.submitted:
    st.success("You have already submitted your details in this session.")
    st.stop()

# Patient Form
# submit = False
with st.form("Patient Dashboard"):

    name = st.text_input("Name")

    col1, col2 = st.columns(2)
    with col1:
        age = st.number_input("Age", 1, 120)
        height = st.number_input("Height(cm)")
        bp_sys = st.number_input("BP Systolic", 50, 250)
        heart_rate = st.number_input("Heart Rate", 30, 200)
        spo2 = st.number_input("SpO₂", 50, 100)
    with col2:
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        weight = st.number_input("Weight(kg)")
        bp_dia = st.number_input("BP Diastolic", 30, 150)
        glucose = st.number_input("Glucose", 50, 400)
        temp = st.number_input("Temperature (°F)", 90.0, 110.0)

    symptoms = st.multiselect(
        "Select symptoms",
        ["Fever", "Cough", "Fatigue", "Chest Pain",
         "Headache", "Breathlessness", "Nausea", "Dizziness", "None"]
    )
    symptoms = ", ".join(symptoms)


    submit = st.form_submit_button("Submit for Analysis")


if submit and not st.session_state.submitted:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="dbda",
        database="medguard"
    )

    cur = conn.cursor()

    cur.execute("""
            INSERT INTO patients(name, age,gender, height, weight, temp, bp_sys,bp_dia,heart_rate,spo2,glucose, symptoms)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (name, age,gender, height, weight, temp,bp_sys,bp_dia,heart_rate,spo2,glucose, symptoms))

    conn.commit()
    cur.close()
    conn.close()
    st.session_state.submitted = True
    st.success("Data submitted successfully!")



# if st.session_state.submitted:
#     st.info("You have already submitted your details in this session.")






# def load_data():
#     conn = mysql.connector.connect(
#         host = "localhost",
#         user = "root",
#         password = "dbda",
#         database = "medguard"
#     )

# components.iframe(
#         "https://console.dialogflow.com/api-client/demo/embedded/9cb88b5f-0915-41e8-ae6e-42e2875a3876",        height=500,
#             width=350
#         )