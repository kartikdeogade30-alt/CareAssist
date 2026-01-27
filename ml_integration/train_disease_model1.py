import warnings
warnings.filterwarnings("ignore")

import joblib
import pandas as pd
import numpy as np
from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, f1_score

from xgboost import XGBClassifier

# ==================================================
# PATH SETUP
# ==================================================
BASE_DIR = Path(__file__).resolve().parent

# DATA LOCATION (UPDATED AS PER YOUR STRUCTURE)
DATASET_PATH = BASE_DIR.parent / "data" / "raw_data" / "dataset.csv"

# MODEL OUTPUT LOCATION
MODEL_DIR = BASE_DIR / "disease_model_1"
MODEL_DIR.mkdir(parents=True, exist_ok=True)

MODEL_PATH = MODEL_DIR / "disease_model.pkl"
ENCODER_PATH = MODEL_DIR / "label_encoder.pkl"
SYMPTOM_COLS_PATH = MODEL_DIR / "symptom_columns.pkl"
SYMPTOMS_TXT_PATH = MODEL_DIR / "symptoms.txt"

# ==================================================
# LOAD DATA
# ==================================================
print(" Loading dataset...")
print(" Dataset path:", DATASET_PATH)

if not DATASET_PATH.exists():
    raise FileNotFoundError(f"Dataset not found at {DATASET_PATH}")

df = pd.read_csv(DATASET_PATH)

# --------------------------------------------------
# CLEAN DATA
# --------------------------------------------------
df.columns = df.columns.str.strip()

for col in df.columns:
    df[col] = df[col].astype(str).str.strip()
    df[col] = df[col].replace("nan", "")

if "Disease" not in df.columns:
    raise ValueError("Dataset must contain a 'Disease' column")

# ==================================================
# BUILD SYMPTOM FEATURE MATRIX
# ==================================================
print(" Building symptom feature matrix...")

symptom_columns = sorted(
    {s for s in df.iloc[:, 1:].values.flatten() if s}
)

X = pd.DataFrame(0, index=df.index, columns=symptom_columns)

for i in range(len(df)):
    for symptom in df.iloc[i, 1:]:
        if symptom:
            X.at[i, symptom] = 1

# Remove rare symptoms (less than 3% occurrence)
min_occurrence = int(0.03 * len(X))
X = X.loc[:, X.sum(axis=0) >= min_occurrence]

print(f" Using {X.shape[1]} symptom features")

# ==================================================
# LABEL ENCODING
# ==================================================
label_encoder = LabelEncoder()
y = label_encoder.fit_transform(df["Disease"])

joblib.dump(label_encoder, ENCODER_PATH)
joblib.dump(list(X.columns), SYMPTOM_COLS_PATH)

with open(SYMPTOMS_TXT_PATH, "w") as f:
    for s in X.columns:
        f.write(s + "\n")

# ==================================================
# TRAIN / TEST SPLIT
# ==================================================
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.3,
    random_state=42,
    stratify=y
)

# ==================================================
# TRAIN XGBOOST MODEL
# ==================================================
print(" Training XGBoost disease model...")

num_classes = len(np.unique(y))

model = XGBClassifier(
    objective="multi:softprob",
    num_class=num_classes,
    n_estimators=300,
    max_depth=6,
    learning_rate=0.05,
    subsample=0.8,
    colsample_bytree=0.8,
    eval_metric="mlogloss",
    random_state=42,
    n_jobs=-1
)

model.fit(X_train, y_train)

# ==================================================
# EVALUATION
# ==================================================
y_pred = model.predict(X_test)

acc = accuracy_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred, average="weighted")

print(f"Accuracy : {acc:.4f}")
print(f"F1 Score : {f1:.4f}")

# ==================================================
# SAVE MODEL
# ==================================================
joblib.dump(model, MODEL_PATH)

print("\n TRAINING COMPLETE")
print(" Files created:")
print(f" - {MODEL_PATH}")
print(f" - {ENCODER_PATH}")
print(f" - {SYMPTOM_COLS_PATH}")
print(f" - {SYMPTOMS_TXT_PATH}")
