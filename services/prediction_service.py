import json
from database.db_connection import get_connection

from ml_integration.feature_builder import build_features
from ml_integration.risk_model import predict_risk
from ml_integration.disease_model import predict_disease

from services.doctor_assignment_service import assign_doctor_for_consultation
from services.precaution_service import get_precautions_for_disease


def generate_and_store_prediction(consultation_id):
    print(f"[AI] Triggered for consultation {consultation_id}")

    try:
        features = build_features(consultation_id)

        # ---------------- VITALS RISK ----------------
        vitals_risk = {"status": "NOT_AVAILABLE"}

        try:
            required = [
                "age", "gender", "height", "weight",
                "temperature", "systolic_bp", "diastolic_bp",
                "heart_rate", "spo2"
            ]

            missing = [k for k in required if features.get(k) is None]
            if missing:
                raise ValueError(f"Missing vitals fields: {missing}")

            risk_features = {
                "age": int(features["age"]),
                "gender": features["gender"],
                "height": float(features["height"]),
                "weight": float(features["weight"]),
                "temperature": float(features["temperature"]),
                "systolic_bp": int(features["systolic_bp"]),
                "diastolic_bp": int(features["diastolic_bp"]),
                "heart_rate": int(features["heart_rate"]),
                "spO2": float(features["spo2"]),
                "bmi": round(
                    float(features["weight"])
                    / ((float(features["height"]) / 100) ** 2),
                    2,
                ),
            }

            risk_level = predict_risk(risk_features)
            vitals_risk = {"status": "AVAILABLE", "risk_level": risk_level}

        except Exception as e:
            print(f"[AI] Vitals risk failed: {e}")

        # ---------------- DISEASE ----------------
        disease_prediction = {"status": "NOT_AVAILABLE"}

        try:
            symptoms = features.get("symptoms", [])

            if symptoms:
                result = predict_disease(symptoms)
                primary = result.get("primary_disease")

                precautions = get_precautions_for_disease(primary)

                disease_prediction = {
                    "status": "AVAILABLE",
                    "primary_disease": primary,
                    "predictions": result.get("predictions", []),
                    "precautions": precautions
                }

        except Exception as e:
            print(f"[AI] Disease prediction failed: {e}")

        # ---------------- STORE ----------------
        prediction_json = {
            "vitals_risk": vitals_risk,
            "disease_prediction": disease_prediction,
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

        # ---------------- ASSIGN DOCTOR ----------------
        assigned_doctor_id = assign_doctor_for_consultation(consultation_id)
        print(f"[AI] Prediction stored & doctor assigned (ID: {assigned_doctor_id})")

    except Exception as e:
        print(f"[AI ERROR] {e}")
