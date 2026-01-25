import json
from database.db_connection import get_connection
from ml_integration.feature_builder import build_features
from ml_integration.risk_model import predict_risk

def generate_and_store_prediction(consultation_id):
    print(f"[AI] Triggered for consultation {consultation_id}")

    try:
        features = build_features(consultation_id)
        print(f"[AI] Features: {features}")

        if features is None:
            prediction = {
                "risk_level": "NOT_AVAILABLE",
                "reason": "Insufficient patient vitals for AI prediction"
            }
        else:
            risk_level = predict_risk(features)
            prediction = {
                "risk_level": risk_level
            }

        print(f"[AI] Prediction payload: {prediction}")

        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            UPDATE consultations
            SET prediction_json = %s
            WHERE consultation_id = %s
        """, (json.dumps(prediction), consultation_id))

        print(f"[AI] Rows affected: {cur.rowcount}")

        conn.commit()
        cur.close()
        conn.close()

        print(f"[AI] Prediction stored successfully")

    except Exception as e:
        print(f"[AI ERROR] {e}")
