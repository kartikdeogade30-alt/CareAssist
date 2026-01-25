import json
from database.db_connection import get_connection
from ml_integration.feature_builder import build_features
from ml_integration.risk_model import predict_risk

def generate_and_store_prediction(consultation_id):
    try:
        features = build_features(consultation_id)
        risk_level = predict_risk(features)

        prediction = {
            "risk_level": risk_level,
        }

        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            UPDATE consultations
            SET prediction_json = %s
            WHERE consultation_id = %s
              AND prediction_json IS NULL
        """, (json.dumps(prediction), consultation_id))

        conn.commit()
        cur.close()
        conn.close()

    except Exception as e:
        print(f"[ML ERROR] Consultation {consultation_id}: {e}")
