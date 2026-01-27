import joblib
import numpy as np
from pathlib import Path

# -------------------------------------------------
# LOAD XGBOOST DISEASE MODEL (NEW)
# -------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent

# 🔥 IMPORTANT: use the new folder
MODEL_DIR = BASE_DIR / "disease_model_1"

MODEL_PATH = MODEL_DIR / "disease_model.pkl"
SYMPTOMS_PATH = MODEL_DIR / "symptom_columns.pkl"
ENCODER_PATH = MODEL_DIR / "label_encoder.pkl"

# Safety checks
if not MODEL_PATH.exists():
    raise FileNotFoundError(f"Missing model file: {MODEL_PATH}")
if not SYMPTOMS_PATH.exists():
    raise FileNotFoundError(f"Missing symptom columns file: {SYMPTOMS_PATH}")
if not ENCODER_PATH.exists():
    raise FileNotFoundError(f"Missing label encoder file: {ENCODER_PATH}")

disease_model = joblib.load(MODEL_PATH)
symptom_columns = joblib.load(SYMPTOMS_PATH)
label_encoder = joblib.load(ENCODER_PATH)

TOP_K = 3

# -------------------------------------------------
# DISEASE PREDICTION
# -------------------------------------------------
def predict_disease(symptoms: list) -> dict:


    if not symptoms:
        raise ValueError("No symptoms provided for disease prediction")

    # Normalize input symptoms
    symptom_set = {s.lower().strip() for s in symptoms}

    # One-hot input vector
    X = np.zeros((1, len(symptom_columns)))

    for idx, col in enumerate(symptom_columns):
        if col.lower().strip() in symptom_set:
            X[0, idx] = 1

    # Predict probabilities
    probs = disease_model.predict_proba(X)[0]

    top_idx = np.argsort(probs)[::-1][:TOP_K]

    predictions = []
    for idx in top_idx:
        predictions.append({
            "disease": label_encoder.inverse_transform([idx])[0],
            "confidence": round(float(probs[idx]), 4)
        })
    print("🧠 Disease model loaded from:", MODEL_PATH)

    return {
        "primary_disease": predictions[0]["disease"],
        "predictions": predictions
    }
