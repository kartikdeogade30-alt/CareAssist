import mysql.connector
import streamlit as st

def get_connection():
    try:
        host = st.secrets["DB_HOST"]
        user = st.secrets["DB_USER"]
        password = st.secrets["DB_PASSWORD"]
        database = st.secrets["DB_NAME"]
        port = int(st.secrets.get("DB_PORT", 3306))
    except KeyError as e:
        raise RuntimeError(f"Missing DB secret: {e}")

    return mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database,
        port=port,
        autocommit=False
    )
