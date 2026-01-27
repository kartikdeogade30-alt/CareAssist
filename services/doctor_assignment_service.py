from database.db_connection import get_connection


def assign_doctor_for_consultation(consultation_id):

    conn = get_connection()
    cur = conn.cursor(dictionary=True)

    try:
        # -----------------------------------
        # 1. Get symptom categories
        # -----------------------------------
        cur.execute("""
            SELECT sm.category
            FROM consultation_symptoms cs
            JOIN symptoms_master sm
              ON sm.symptom_id = cs.symptom_id
            WHERE cs.consultation_id = %s
        """, (consultation_id,))

        rows = cur.fetchall()

        # -----------------------------------
        # 2. Decide specialization
        # -----------------------------------
        if not rows:
            specialization = "GENERAL"
        else:
            freq = {}
            for r in rows:
                cat = r["category"]
                freq[cat] = freq.get(cat, 0) + 1

            specialization = max(freq, key=freq.get)

        # -----------------------------------
        # 3. Pick doctor
        # -----------------------------------
        cur.execute("""
            SELECT doctor_id
            FROM doctors
            WHERE specialization = %s
            ORDER BY years_of_experience DESC
            LIMIT 1
        """, (specialization,))

        doc = cur.fetchone()

        if not doc:
            # fallback to GENERAL
            cur.execute("""
                SELECT doctor_id
                FROM doctors
                WHERE specialization = 'GENERAL'
                ORDER BY years_of_experience DESC
                LIMIT 1
            """)
            doc = cur.fetchone()

        doctor_id = doc["doctor_id"]

        # -----------------------------------
        # 4. Assign doctor to consultation
        # -----------------------------------
        cur.execute("""
            UPDATE consultations
            SET doctor_id = %s
            WHERE consultation_id = %s
        """, (doctor_id, consultation_id))

        conn.commit()
        return doctor_id

    finally:
        cur.close()
        conn.close()
