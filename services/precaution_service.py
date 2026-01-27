from database.db_connection import get_connection


def get_precautions_for_disease(disease_name: str):

    if not disease_name:
        return []

    conn = get_connection()
    cur = conn.cursor(dictionary=True)

    cur.execute("""
        SELECT dp.precaution_text
        FROM diseases d
        JOIN disease_precautions dp
            ON dp.disease_id = d.disease_id
        WHERE LOWER(d.disease_name) = LOWER(%s)
        ORDER BY dp.precaution_order
    """, (disease_name,))

    rows = cur.fetchall()
    cur.close()
    conn.close()

    return [r["precaution_text"] for r in rows]
