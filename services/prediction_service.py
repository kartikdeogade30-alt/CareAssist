import json
from database.db_connection import get_connection
from ml_integration.feature_builder import build_features
from ml_integration.risk_model import predict_risk
from ml_integration.disease_model import predict_disease

def generate_and_store_prediction(consultation_id):
    print(f"[AI] Triggered for consultation {consultation_id}")

    try:
        features = build_features(consultation_id)

        risk_level = predict_risk(features)
        disease_result = predict_disease(features["symptoms"])

        prediction = {
            "risk_level": risk_level,
            "disease_prediction": disease_result
        }

        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            UPDATE consultations
            SET prediction_json = %s
            WHERE consultation_id = %s
        """, (json.dumps(prediction), consultation_id))

        conn.commit()
        cur.close()
        conn.close()

        print("[AI] Risk & Disease prediction stored successfully")

    except Exception as e:
        print(f"[AI ERROR] {e}")
