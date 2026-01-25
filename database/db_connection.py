import mysql.connector
import os
import streamlit as st

def get_connection():
    host = st.secrets.get("DB_HOST") or os.getenv("DB_HOST")
    user = st.secrets.get("DB_USER") or os.getenv("DB_USER")
    password = st.secrets.get("DB_PASSWORD") or os.getenv("DB_PASSWORD")
    database = st.secrets.get("DB_NAME") or os.getenv("DB_NAME")
    port = st.secrets.get("DB_PORT") or os.getenv("DB_PORT", 3306)

    return mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database,
        port=int(port),
        autocommit=False
    )
