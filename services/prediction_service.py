import json
from database.db_connection import get_connection

from ml_integration.feature_builder import build_features
from ml_integration.risk_model import predict_risk
from ml_integration.disease_model import predict_disease
from services.doctor_assignment_service import assign_doctor_for_consultation


def generate_and_store_prediction(consultation_id):
    print(f"[AI] Triggered for consultation {consultation_id}")

    try:
        # ==================================================
        # BUILD FEATURES (SINGLE SOURCE OF TRUTH)
        # ==================================================
        features = build_features(consultation_id)

        # ==================================================
        # VITALS RISK
        # ==================================================
        vitals_risk = {"status": "NOT_AVAILABLE"}

        try:
            # Minimal, sane validation
            required = [
                "age",
                "gender",
                "height",
                "weight",
                "temperature",
                "systolic_bp",
                "diastolic_bp",
                "heart_rate",
                "spo2",
            ]

            missing = [k for k in required if not features.get(k)]
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

            print("🔎 VITAL FEATURES:", risk_features)

            risk_level = predict_risk(risk_features)

            vitals_risk = {
                "status": "AVAILABLE",
                "risk_level": risk_level,
            }

            print(f"[AI] Vitals risk computed: {risk_level}")

        except Exception as e:
            print(f"[AI] Vitals risk failed: {e}")

        # ==================================================
        # DISEASE PREDICTION (SYMPTOMS ONLY)
        # ==================================================
        disease_prediction = {"status": "NOT_AVAILABLE"}

        try:
            symptoms = features.get("symptoms", [])

            if symptoms:
                result = predict_disease(symptoms)

                disease_prediction = {
                    "status": "AVAILABLE",
                    "primary_disease": result.get("primary_disease"),
                    "predictions": result.get("predictions", []),
                }

                print(f"[AI] Disease predicted: {result.get('primary_disease')}")

        except Exception as e:
            print(f"[AI] Disease prediction failed: {e}")

        # ==================================================
        # STORE FINAL JSON
        # ==================================================
        prediction_json = {
            "vitals_risk": vitals_risk,
            "disease_prediction": disease_prediction,
        }

        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            """
            UPDATE consultations
            SET prediction_json = %s
            WHERE consultation_id = %s
            """,
            (json.dumps(prediction_json), consultation_id),
        )

        conn.commit()
        cur.close()
        conn.close()

        # ==================================================
        # DOCTOR ASSIGNMENT
        # ==================================================
        assigned_doctor_id = assign_doctor_for_consultation(consultation_id)
        print(f"[AI] Prediction stored & doctor assigned (ID: {assigned_doctor_id})")

    except Exception as e:
        print(f"[AI ERROR] {e}")
