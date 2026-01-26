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
        # VITALS RISK MODEL (Vitals ONLY)
        # -------------------------------
        try:
            risk_features = {
                "age": features["age"],
                "gender": features["gender"],
                "height": features["height"],
                "weight": features["weight"],
                "temperature": features["temperature"],
                "systolic_bp": features["systolic_bp"],
                "diastolic_bp": features["diastolic_bp"],
                "blood_sugar": features["blood_sugar"],
                "heart_rate": features["heart_rate"],
                "spo2": features["spo2"]
            }

            risk_level = predict_risk(risk_features)

            vitals_risk = {
                "status": "AVAILABLE",
                "risk_level": risk_level
            }
        except Exception as e:
            print(f"[AI] Vitals risk failed: {e}")
            vitals_risk = {"status": "NOT_AVAILABLE"}

        # -------------------------------
        # DISEASE MODEL (STRING INPUT)
        # -------------------------------
        try:
            if features["symptoms"]:
                symptom_text = ", ".join(features["symptoms"])
                result = predict_disease(symptom_text)

                disease_prediction = {
                    "status": "AVAILABLE",
                    "primary_disease": result.get("primary_disease"),
                    "predictions": result.get("predictions", [])
                }
            else:
                disease_prediction = {"status": "NOT_AVAILABLE"}
        except Exception as e:
            print(f"[AI] Disease prediction failed: {e}")
            disease_prediction = {"status": "NOT_AVAILABLE"}

        # -------------------------------
        # STORE JSON
        # -------------------------------
        prediction_json = {
            "vitals_risk": vitals_risk,
            "disease_prediction": disease_prediction
        }

        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            UPDATE consultations
            SET prediction_json = %s
            WHERE consultation_id = %s
        """, (json.dumps(prediction_json), consultation_id))
        conn.commit()

        cur.close()
        conn.close()

        print("[AI] Prediction stored successfully")

    except Exception as e:
        print(f"[AI ERROR] {e}")
