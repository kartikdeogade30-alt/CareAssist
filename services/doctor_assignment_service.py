from database.db_connection import get_connection


# ==================================================
# DISEASE → SPECIALIZATION MAP
# (Must match doctors.specialization exactly)
# ==================================================
DISEASE_SPECIALIZATION_MAP = {
    # Allergic / Drug
    "Drug Reaction": "GENERAL",
    "Allergy": "DERMATOLOGICAL",

    # Infectious
    "Malaria": "INFECTIOUS",
    "Typhoid": "INFECTIOUS",
    "Chicken pox": "INFECTIOUS",
    "Dengue": "INFECTIOUS",
    "Tuberculosis": "INFECTIOUS",
    "Pneumonia": "RESPIRATORY",
    "Common Cold": "RESPIRATORY",

    # Endocrine / Metabolic
    "Hypothyroidism": "ENDOCRINE_METABOLIC",
    "Hyperthyroidism": "ENDOCRINE_METABOLIC",
    "Diabetes": "ENDOCRINE_METABOLIC",
    "Hypoglycemia": "ENDOCRINE_METABOLIC",

    # Dermatological
    "Psoriasis": "DERMATOLOGICAL",
    "Acne": "DERMATOLOGICAL",
    "Impetigo": "DERMATOLOGICAL",
    "Fungal infection": "DERMATOLOGICAL",

    # Gastrointestinal
    "GERD": "GASTROINTESTINAL",
    "Peptic ulcer diseae": "GASTROINTESTINAL",
    "Dimorphic hemmorhoids(piles)": "GASTROINTESTINAL",
    "Gastroenteritis": "GASTROINTESTINAL",

    # Hepatic
    "Chronic cholestasis": "HEPATIC",
    "hepatitis A": "HEPATIC",
    "Hepatitis B": "HEPATIC",
    "Hepatitis C": "HEPATIC",
    "Hepatitis D": "HEPATIC",
    "Hepatitis E": "HEPATIC",
    "Alcoholic hepatitis": "HEPATIC",
    "Jaundice": "HEPATIC",

    # Musculoskeletal / Ortho
    "Osteoarthristis": "MUSCULOSKELETAL",
    "Arthritis": "MUSCULOSKELETAL",
    "Cervical spondylosis": "MUSCULOSKELETAL",

    # Neurological
    "(vertigo) Paroymsal  Positional Vertigo": "NEUROLOGICAL",
    "Paralysis (brain hemorrhage)": "NEUROLOGICAL",
    "Migraine": "NEUROLOGICAL",

    # Urological
    "Urinary tract infection": "UROLOGICAL",

    # Vascular / Cardio
    "Varicose veins": "VASCULAR",
    "Heart attack": "CARDIOVASCULAR",
    "Hypertension": "CARDIOVASCULAR",

    # Respiratory
    "Bronchial Asthma": "RESPIRATORY",

    # Others
    "AIDS": "GENERAL",
}


# ==================================================
# ASSIGN DOCTOR BASED ON PRIMARY DISEASE
# ==================================================
def assign_doctor_for_consultation(consultation_id):
    conn = get_connection()
    cur = conn.cursor(dictionary=True)

    try:
        # ------------------------------------------
        # GET PRIMARY DISEASE
        # ------------------------------------------
        cur.execute("""
            SELECT prediction_json
            FROM consultations
            WHERE consultation_id = %s
        """, (consultation_id,))

        row = cur.fetchone()
        if not row or not row["prediction_json"]:
            specialization = "GENERAL"
        else:
            prediction = row["prediction_json"]
            if isinstance(prediction, str):
                import json
                prediction = json.loads(prediction)

            primary_disease = (
                prediction
                .get("disease_prediction", {})
                .get("primary_disease")
            )

            specialization = DISEASE_SPECIALIZATION_MAP.get(
                primary_disease,
                "GENERAL"
            )

        # ------------------------------------------
        # FIND AVAILABLE DOCTOR
        # ------------------------------------------
        cur.execute("""
            SELECT doctor_id
            FROM doctors
            WHERE specialization = %s
            ORDER BY years_of_experience DESC
            LIMIT 1
        """, (specialization,))

        doctor = cur.fetchone()

        if not doctor:
            # fallback to general physician
            cur.execute("""
                SELECT doctor_id
                FROM doctors
                WHERE specialization = 'GENERAL'
                LIMIT 1
            """)
            doctor = cur.fetchone()

        if doctor:
            cur.execute("""
                UPDATE consultations
                SET doctor_id = %s
                WHERE consultation_id = %s
            """, (doctor["doctor_id"], consultation_id))

            conn.commit()
            return doctor["doctor_id"]

        return None

    finally:
        cur.close()
        conn.close()
