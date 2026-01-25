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

# ---------------- PREDICT ----------------
def predict_risk(features: dict) -> str:
    """
    Uses STACKING ENSEMBLE
    """

    X = pd.DataFrame([{
        "Heart Rate": features["heart_rate"],
        "Body Temperature": features["temperature"],
        "Oxygen Saturation": features["spO2"],
        "Systolic Blood Pressure": features["systolic_bp"],
        "Diastolic Blood Pressure": features["diastolic_bp"],
        "Age": features["age"],
        "Gender": 1 if features["gender"] == "MALE" else 0,
        "Weight (kg)": features["weight_kg"],
        "Height (m)": features["height_cm"] / 100,
        "Derived_BMI": features["bmi"]
    }])

    # Base model probabilities
    xgb_prob = xgb_model.predict_proba(X)[0][1]
    cat_prob = cat_model.predict_proba(X)[0][1]
    lgb_prob = lgb_model.predict_proba(X)[0][1]

    # Meta model
    meta_X = np.array([[xgb_prob, cat_prob, lgb_prob]])
    final_prob = meta_model.predict_proba(meta_X)[0][1]

    return "HIGH" if final_prob >= THRESHOLD else "LOW"
