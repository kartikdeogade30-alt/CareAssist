from database.db_connection import get_connection

def log_login_event(user_type: str, user_id: int, status: str):

    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            INSERT INTO login_audit_logs (user_type, user_id, login_status)
            VALUES (%s, %s, %s)
        """, (user_type, user_id, status))
        conn.commit()
    except Exception as e:
        conn.rollback()
        print("Login audit log error:", e)
    finally:
        cur.close()
        conn.close()
