# ==================================================
# TRAIN & SAVE STACKING MODEL (ONE-TIME SCRIPT)
# ==================================================

import numpy as np
import pandas as pd
import joblib
from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

import xgboost as xgb
import catboost as cb
import lightgbm as lgb

# ==================================================
# PATH CONFIG (ROBUST & PORTABLE)
# ==================================================

# This file -> ml_integration/train_stacking_model.py
# Project root -> CareAssist/

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_PATH = BASE_DIR / "data" / "raw_data" / "human_vital_signs_dataset_2024.csv"
MODEL_DIR = BASE_DIR / "ml_integration" / "stacking_model"
MODEL_DIR.mkdir(exist_ok=True)

print("Project root :", BASE_DIR)
print("Dataset path :", DATA_PATH)
print("Model dir    :", MODEL_DIR)

# ==================================================
# LOAD DATA
# ==================================================

df = pd.read_csv(DATA_PATH)

FEATURES = [
    "Heart Rate",
    "Body Temperature",
    "Oxygen Saturation",
    "Systolic Blood Pressure",
    "Diastolic Blood Pressure",
    "Age",
    "Gender",
    "Weight (kg)",
    "Height (m)",
    "Derived_BMI"
]

TARGET = "Risk Category"

# ==================================================
# PREPROCESS
# ==================================================

# Encode Gender
df["Gender"] = df["Gender"].map({"Male": 1, "Female": 0})

# Encode Target
df["Risk"] = df[TARGET].map({
    "Low Risk": 0,
    "High Risk": 1
})

X = df[FEATURES]
y = df["Risk"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

print(f"Training samples: {len(X_train)}")
print(f"Testing samples : {len(X_test)}")

# ==================================================
# BASE MODELS
# ==================================================

print("\nTraining base models...")

xgb_model = xgb.XGBClassifier(
    n_estimators=100,
    max_depth=6,
    learning_rate=0.1,
    random_state=42,
    use_label_encoder=False,
    eval_metric="logloss"
)

cat_model = cb.CatBoostClassifier(
    iterations=100,
    depth=6,
    learning_rate=0.1,
    random_seed=42,
    verbose=0
)

lgb_model = lgb.LGBMClassifier(
    n_estimators=100,
    random_state=42
)

xgb_model.fit(X_train, y_train)
cat_model.fit(X_train, y_train, cat_features=["Gender"])
lgb_model.fit(X_train, y_train)

# ==================================================
# META MODEL (STACKING)
# ==================================================

print("\nTraining meta model...")

xgb_prob = xgb_model.predict_proba(X_test)[:, 1]
cat_prob = cat_model.predict_proba(X_test)[:, 1]
lgb_prob = lgb_model.predict_proba(X_test)[:, 1]

meta_X = np.column_stack([xgb_prob, cat_prob, lgb_prob])

meta_model = LogisticRegression()
meta_model.fit(meta_X, y_test)

meta_acc = accuracy_score(y_test, meta_model.predict(meta_X))
print(f"Meta model accuracy: {meta_acc:.4f}")

# ==================================================
# SAVE MODELS
# ==================================================

print("\nSaving models...")

joblib.dump(xgb_model, MODEL_DIR / "xgb_model.pkl")
joblib.dump(cat_model, MODEL_DIR / "cat_model.pkl")
joblib.dump(lgb_model, MODEL_DIR / "lgb_model.pkl")
joblib.dump(meta_model, MODEL_DIR / "meta_model.pkl")

with open(MODEL_DIR / "features.txt", "w") as f:
    for feat in FEATURES:
        f.write(feat + "\n")

print("\n✅ STACKING MODEL TRAINED & SAVED SUCCESSFULLY")
print("Saved files:")
print(" - xgb_model.pkl")
print(" - cat_model.pkl")
print(" - lgb_model.pkl")
print(" - meta_model.pkl")
print(" - features.txt")
