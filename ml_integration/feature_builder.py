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
        SELECT sm.symptom_name
        FROM consultation_symptoms cs
        JOIN symptoms_master sm
            ON sm.symptom_id = cs.symptom_id
        WHERE cs.consultation_id = %s
    """, (consultation_id,))
    symptoms = [row["symptom_name"] for row in cur.fetchall()]

    cur.close()
    conn.close()

    # ---------------- Validation ----------------
    if not patient or not vitals:
        return None

    required_vitals = [
        vitals["heart_rate"],
        vitals["temperature_c"],
        vitals["spO2"],
        vitals["systolic_bp"],
        vitals["diastolic_bp"],
        vitals["weight_kg"],
        vitals["height_cm"],
    ]

    if any(v is None for v in required_vitals):
        return None

    # ---------------- Feature Engineering ----------------
    dob = patient["date_of_birth"]
    today = date.today()
    age = today.year - dob.year - (
        (today.month, today.day) < (dob.month, dob.day)
    )

    bmi = vitals["weight_kg"] / ((vitals["height_cm"] / 100) ** 2)

    return {
        # --- Demographics ---
        "age": int(age),
        "gender": patient["gender"],

        # --- Vitals (Risk model) ---
        "heart_rate": float(vitals["heart_rate"]),
        "temperature": float(vitals["temperature_c"]),
        "spO2": float(vitals["spO2"]),
        "systolic_bp": float(vitals["systolic_bp"]),
        "diastolic_bp": float(vitals["diastolic_bp"]),
        "weight_kg": float(vitals["weight_kg"]),
        "height_cm": float(vitals["height_cm"]),
        "bmi": round(float(bmi), 2),

        # --- Symptoms (Disease model) ---
        "symptoms": symptoms  # safe even if empty
    }
