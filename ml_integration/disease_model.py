import joblib
import pandas as pd
import numpy as np
from pathlib import Path

BASE_DIR = Path("ml_integration")
MODEL_DIR = BASE_DIR / "disease_model"

disease_model = joblib.load(MODEL_DIR / "disease_model.pkl")
symptom_columns = joblib.load(MODEL_DIR / "symptom_columns.pkl")
label_encoder = joblib.load(MODEL_DIR / "label_encoder.pkl")

TOP_K = 3

def predict_disease(symptoms: list) -> dict:
    X = pd.DataFrame(0, index=[0], columns=symptom_columns)

    for symptom in symptoms:
        if symptom in X.columns:
            X.at[0, symptom] = 1

    probs = disease_model.predict_proba(X)[0]
    top_idx = np.argsort(probs)[::-1][:TOP_K]

    predictions = []
    for idx in top_idx:
        predictions.append({
            "disease": label_encoder.inverse_transform([idx])[0],
            "confidence": round(float(probs[idx]), 4)
        })

    return {
        "primary_disease": predictions[0]["disease"],
        "predictions": predictions
    }
