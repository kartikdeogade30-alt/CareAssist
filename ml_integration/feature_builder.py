from database.db_connection import get_connection
from datetime import date

def build_features(consultation_id):
    conn = get_connection()
    cur = conn.cursor(dictionary=True)

    # ---------------- Patient Info ----------------
    cur.execute("""
        SELECT p.date_of_birth, p.gender
        FROM consultations c
        JOIN patients p ON p.patient_id = c.patient_id
        WHERE c.consultation_id = %s
    """, (consultation_id,))
    patient = cur.fetchone()

    # ---------------- Vitals ----------------
    cur.execute("""
        SELECT *
        FROM patient_vitals
        WHERE consultation_id = %s
    """, (consultation_id,))
    vitals = cur.fetchone()

    # ---------------- Symptoms ----------------
    cur.execute("""
        SELECT symptom_name
        FROM consultation_symptoms
        WHERE consultation_id = %s
    """, (consultation_id,))
    symptoms = [row["symptom_name"] for row in cur.fetchall()]

    cur.close()
    conn.close()

    if not patient or not vitals:
        raise ValueError("Incomplete data for feature building")

    # Accurate age calculation
    dob = patient["date_of_birth"]
    today = date.today()
    age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))

    bmi = vitals["weight_kg"] / ((vitals["height_cm"] / 100) ** 2)

    return {
        "age": age,
        "gender": patient["gender"],

        "heart_rate": vitals["heart_rate"],
        "temperature": vitals["temperature_c"],
        "spO2": vitals["spO2"],

        "systolic_bp": vitals["systolic_bp"],
        "diastolic_bp": vitals["diastolic_bp"],

        "weight_kg": vitals["weight_kg"],
        "height_cm": vitals["height_cm"],

        "bmi": round(bmi, 2),

        # NEW
        "symptoms": symptoms
    }
