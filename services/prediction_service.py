import json
from database.db_connection import get_connection
from ml_integration.feature_builder import build_features
from ml_integration.risk_model import predict_risk
from ml_integration.disease_model import predict_disease

def generate_and_store_prediction(consultation_id):
    print(f"[AI] Triggered for consultation {consultation_id}")

    try:
        features = build_features(consultation_id)

        # -------------------------------
        # VITALS RISK MODEL
        # -------------------------------
        try:
            risk_level = predict_risk(features)
            vitals_risk = {
                "status": "AVAILABLE",
                "risk_level": risk_level
            }
        except Exception as e:
            print(f"[AI] Vitals risk unavailable: {e}")
            vitals_risk = {
                "status": "NOT_AVAILABLE"
            }

        # -------------------------------
        # DISEASE PREDICTION MODEL
        # -------------------------------
        try:
            if features.get("symptoms"):
                disease_result = predict_disease(features["symptoms"])
                disease_prediction = {
                    "status": "AVAILABLE",
                    "primary_disease": disease_result.get("primary_disease"),
                    "predictions": disease_result.get("predictions", [])
                }
            else:
                disease_prediction = {
                    "status": "NOT_AVAILABLE"
                }
        except Exception as e:
            print(f"[AI] Disease prediction unavailable: {e}")
            disease_prediction = {
                "status": "NOT_AVAILABLE"
            }

        # -------------------------------
        # FINAL PREDICTION JSON
        # -------------------------------
        prediction = {
            "vitals_risk": vitals_risk,
            "disease_prediction": disease_prediction
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

        print("[AI] Prediction JSON stored successfully")

    except Exception as e:
        print(f"[AI ERROR] {e}")
