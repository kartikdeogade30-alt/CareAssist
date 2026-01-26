from database.db_connection import get_connection

# -------------------------------------------------
# UTILITIES
# -------------------------------------------------
def fahrenheit_to_celsius(f):
    return round((f - 32) * 5 / 9, 2)



def build_features(consultation_id):
    conn = get_connection()
    cur = conn.cursor(dictionary=True)

    try:
        # -------------------------------
        # VITALS
        # -------------------------------
        cur.execute("""
            SELECT
                height_cm,
                weight_kg,
                temperature_c,
                systolic_bp,
                diastolic_bp,
                blood_sugar,
                heart_rate,
                spO2
            FROM patient_vitals
            WHERE consultation_id = %s
        """, (consultation_id,))
        vitals = cur.fetchone()

        if not vitals:
            raise ValueError("Vitals not found")

        temperature_c = fahrenheit_to_celsius(vitals["temperature_c"])

        # -------------------------------
        # PATIENT
        # -------------------------------
        cur.execute("""
            SELECT
                p.gender,
                TIMESTAMPDIFF(YEAR, p.date_of_birth, CURDATE()) AS age
            FROM consultations c
            JOIN patients p ON p.patient_id = c.patient_id
            WHERE c.consultation_id = %s
        """, (consultation_id,))
        patient = cur.fetchone()

        if not patient:
            raise ValueError("Patient not found")

        # -------------------------------
        # SYMPTOMS (NAMES)
        # -------------------------------
        cur.execute("""
            SELECT sm.symptom_name
            FROM consultation_symptoms cs
            JOIN symptoms_master sm ON sm.symptom_id = cs.symptom_id
            WHERE cs.consultation_id = %s
        """, (consultation_id,))
        symptoms = [r["symptom_name"] for r in cur.fetchall()]

        return {
            "age": patient["age"],
            "gender": patient["gender"],
            "height": vitals["height_cm"],
            "weight": vitals["weight_kg"],
            "temperature": temperature_c,  # °C for ML
            "systolic_bp": vitals["systolic_bp"],
            "diastolic_bp": vitals["diastolic_bp"],
            "blood_sugar": vitals["blood_sugar"],
            "heart_rate": vitals["heart_rate"],
            "spo2": vitals["spO2"],
            "symptoms": symptoms
        }

    finally:
        cur.close()
        conn.close()
