import joblib
import pandas as pd
import numpy as np
from pathlib import Path

# ---------------- PATHS ----------------
BASE_DIR = Path("ml_integration")
MODEL_DIR = BASE_DIR / "stacking_model"

xgb_model = joblib.load(MODEL_DIR / "xgb_model.pkl")
cat_model = joblib.load(MODEL_DIR / "cat_model.pkl")
lgb_model = joblib.load(MODEL_DIR / "lgb_model.pkl")
meta_model = joblib.load(MODEL_DIR / "meta_model.pkl")

THRESHOLD = 0.5


def calculate_bmi(weight, height):
    return round(float(weight) / ((float(height) / 100) ** 2), 2)


def predict_risk(features: dict) -> str:
    bmi = calculate_bmi(features["weight"], features["height"])

    X = pd.DataFrame([{
        "Heart Rate": float(features["heart_rate"]),
        "Body Temperature": float(features["temperature"]),
        "Oxygen Saturation": float(features["spO2"]),
        "Systolic Blood Pressure": float(features["systolic_bp"]),
        "Diastolic Blood Pressure": float(features["diastolic_bp"]),
        "Age": int(features["age"]),
        "Gender": int(1 if features["gender"] == "MALE" else 0),
        "Weight (kg)": float(features["weight"]),
        "Height (m)": float(features["height"]) / 100,
        "Derived_BMI": float(bmi)
    }])

    # ---- Base models ----
    xgb_prob = float(xgb_model.predict_proba(X)[0][1])
    cat_prob = float(cat_model.predict_proba(X)[0][1])
    lgb_prob = float(lgb_model.predict_proba(X)[0][1])

    # ---- Meta model ----
    meta_X = np.array([[xgb_prob, cat_prob, lgb_prob]], dtype=float)
    final_prob = float(meta_model.predict_proba(meta_X)[0][1])

    return "HIGH" if final_prob >= THRESHOLD else "LOW"
