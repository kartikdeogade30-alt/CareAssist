# ==================================================
# TRAIN & SAVE DISEASE PREDICTION MODEL (ONE-TIME)
# ==================================================

import numpy as np
import pandas as pd
import joblib
from pathlib import Path

from sklearn.model_selection import (
    train_test_split, StratifiedKFold, GridSearchCV
)
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score

import warnings
warnings.filterwarnings("ignore")

# ==================================================
# PATH CONFIG (ROBUST & PORTABLE)
# ==================================================

# This file -> ml_integration/train_disease_model.py
# Project root -> CareAssist/

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_PATH = BASE_DIR / "data" / "raw_data" / "dataset.csv"
MODEL_DIR = BASE_DIR / "ml_integration" / "disease_model"
MODEL_DIR.mkdir(exist_ok=True)

print("Project root :", BASE_DIR)
print("Dataset path :", DATA_PATH)
print("Model dir    :", MODEL_DIR)

# ==================================================
# LOAD DATA
# ==================================================

df = pd.read_csv(DATA_PATH)
print("Dataset shape:", df.shape)

# ==================================================
# CLEAN SYMPTOMS
# ==================================================

for col in df.columns:
    df[col] = df[col].astype(str).str.strip().replace("nan", "")

# ==================================================
# BUILD BINARY SYMPTOM MATRIX
# ==================================================

all_symptoms = sorted(set(df.iloc[:, 1:].values.flatten()))
all_symptoms = [s for s in all_symptoms if s != ""]

X = pd.DataFrame(0, index=df.index, columns=all_symptoms)

for i in range(len(df)):
    for symptom in df.iloc[i, 1:].values:
        if symptom:
            X.loc[i, symptom] = 1

# ==================================================
# DROP RARE SYMPTOMS (ANTI-OVERFITTING)
# ==================================================

min_occurrence = int(0.03 * len(X))  # at least 3% of samples
X = X.loc[:, X.sum(axis=0) >= min_occurrence]

print("Remaining symptoms:", X.shape[1])

# ==================================================
# ENCODE TARGET
# ==================================================

label_encoder = LabelEncoder()
y = label_encoder.fit_transform(df["Disease"])

# Save label encoder
joblib.dump(label_encoder, MODEL_DIR / "label_encoder.pkl")

# ==================================================
# TRAIN / TEST SPLIT
# ==================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.30,
    random_state=42,
    stratify=y
)

print(f"Training samples: {len(X_train)}")
print(f"Testing samples : {len(X_test)}")

# ==================================================
# LOGISTIC REGRESSION (MAX REGULARIZATION)
# ==================================================

base_model = LogisticRegression(
    solver="saga",
    penalty="elasticnet",
    class_weight="balanced",
    multi_class="multinomial",
    max_iter=5000,
    random_state=42
)

param_grid = {
    "C": [0.01, 0.05, 0.1],
    "l1_ratio": [0.3, 0.5, 0.7]
}

cv = StratifiedKFold(
    n_splits=5,
    shuffle=True,
    random_state=42
)

grid = GridSearchCV(
    base_model,
    param_grid,
    scoring="f1_weighted",
    cv=cv,
    n_jobs=-1
)

print("\nTraining disease prediction model...")
grid.fit(X_train, y_train)

best_model = grid.best_estimator_

print("\nBest hyperparameters:")
print(grid.best_params_)

# ==================================================
# EVALUATION
# ==================================================

y_pred = best_model.predict(X_test)

acc = accuracy_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred, average="weighted")

print("\nMODEL PERFORMANCE")
print("=================")
print(f"Accuracy : {acc:.4f}")
print(f"F1-score : {f1:.4f}")

# ==================================================
# SAVE MODEL + FEATURES
# ==================================================

joblib.dump(best_model, MODEL_DIR / "disease_model.pkl")

# Save symptom columns for inference
joblib.dump(list(X.columns), MODEL_DIR / "symptom_columns.pkl")

# Optional: keep human-readable version
with open(MODEL_DIR / "symptoms.txt", "w") as f:
    for symptom in X.columns:
        f.write(symptom + "\n")


print("\n✅ DISEASE MODEL TRAINED & SAVED SUCCESSFULLY")
print("Saved files:")
print(" - disease_model.pkl")
print(" - label_encoder.pkl")
print(" - symptom_columns.pkl")
print(" - symptoms.txt")
