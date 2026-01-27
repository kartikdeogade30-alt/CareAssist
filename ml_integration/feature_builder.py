from database.db_connection import get_connection


def build_features(consultation_id):
    conn = get_connection()
    cur = conn.cursor(dictionary=True)

    try:
        # -------------------------------
        # VITALS (DB IS SOURCE OF TRUTH)
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
        # SYMPTOMS
        # -------------------------------
        cur.execute("""
            SELECT sm.symptom_name
            FROM consultation_symptoms cs
            JOIN symptoms_master sm ON sm.symptom_id = cs.symptom_id
            WHERE cs.consultation_id = %s
        """, (consultation_id,))
        symptoms = [r["symptom_name"] for r in cur.fetchall()]

        # -------------------------------
        # NORMALIZED OUTPUT (FINAL)
        # -------------------------------
        return {
            "age": int(patient["age"]),
            "gender": patient["gender"],

            "height": float(vitals["height_cm"]),
            "weight": float(vitals["weight_kg"]),
            "temperature": float(vitals["temperature_c"]),
            "systolic_bp": int(vitals["systolic_bp"]),
            "diastolic_bp": int(vitals["diastolic_bp"]),
            "heart_rate": int(vitals["heart_rate"]),
            "spo2": int(vitals["spO2"]),

            "symptoms": symptoms
        }

    finally:
        cur.close()
        conn.close()
