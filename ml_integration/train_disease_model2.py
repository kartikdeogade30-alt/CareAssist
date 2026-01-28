import warnings
warnings.filterwarnings("ignore")

import joblib
import pandas as pd
import numpy as np
from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, f1_score

# ==================================================
# PATH SETUP
# ==================================================
BASE_DIR = Path(__file__).resolve().parent

# DATA LOCATION
DATASET_PATH = BASE_DIR.parent / "data" / "raw_data" / "dataset.csv"

# MODEL OUTPUT LOCATION
MODEL_DIR = BASE_DIR / "disease_model_nb"
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
# CLEAN DATA (LIKE PCARF)
# --------------------------------------------------
def clean_symptom(s):
    """Clean symptom string like PCARF"""
    if pd.isna(s):
        return ""
    return str(s).strip().lower().replace(" ", "_")

# Clean all symptom columns
for col in df.columns[1:]:  # Skip Disease column
    df[col] = df[col].apply(clean_symptom)

# Clean Disease column
if "Disease" not in df.columns:
    raise ValueError("Dataset must contain a 'Disease' column")

df["Disease"] = df["Disease"].str.strip()

# ==================================================
# BUILD SYMPTOM FEATURE MATRIX (LIKE PCARF)
# ==================================================
print(" Building symptom feature matrix (PCARF style)...")

# Get all unique symptoms from all symptom columns
all_symptoms = sorted(set(
    symptom
    for col in df.columns[1:]
    for symptom in df[col].unique()
    if symptom != ""
))

print(f" Found {len(all_symptoms)} unique symptoms")

# Create one-hot encoded matrix
X = pd.DataFrame(0, index=df.index, columns=all_symptoms)

for i, row in df.iterrows():
    for col in df.columns[1:]:
        symptom = row[col]
        if symptom and symptom in all_symptoms:
            X.at[i, symptom] = 1

print(f" Feature matrix shape: {X.shape}")

# ==================================================
# LABEL ENCODING
# ==================================================
label_encoder = LabelEncoder()
y = label_encoder.fit_transform(df["Disease"])

# Save components
joblib.dump(label_encoder, ENCODER_PATH)
joblib.dump(list(X.columns), SYMPTOM_COLS_PATH)

# Save symptoms to text file
with open(SYMPTOMS_TXT_PATH, "w", encoding="utf-8") as f:
    for s in X.columns:
        f.write(s + "\n")

print(f" Saved {len(X.columns)} symptom features")

# ==================================================
# TRAIN / TEST SPLIT
# ==================================================
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,  # Like PCARF
    random_state=42,
    stratify=y
)

print(f" Train size: {X_train.shape[0]}, Test size: {X_test.shape[0]}")

# ==================================================
# TRAIN MULTINOMIALNB MODEL (LIKE PCARF)
# ==================================================
print(" Training MultinomialNB disease model...")

# Use same alpha as PCARF
model = MultinomialNB(alpha=0.1)
model.fit(X_train, y_train)

# ==================================================
# EVALUATION
# ==================================================
y_pred = model.predict(X_test)
y_pred_proba = model.predict_proba(X_test)

acc = accuracy_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred, average="weighted")

print("\n" + "="*50)
print(" MODEL EVALUATION")
print("="*50)
print(f" Accuracy : {acc:.4f}")
print(f" F1 Score : {f1:.4f}")

# Show confidence scores for first few predictions
print(f"\n Sample predictions (first 5 test cases):")
for i in range(min(5, len(y_test))):
    true_disease = label_encoder.inverse_transform([y_test[i]])[0]
    pred_disease = label_encoder.inverse_transform([y_pred[i]])[0]
    confidence = max(y_pred_proba[i]) * 100
    
    # Use simple ASCII indicators
    if true_disease == pred_disease:
        print(f"  [OK] True: {true_disease:<20} Pred: {pred_disease:<20} Conf: {confidence:.1f}%")
    else:
        print(f"  [XX] True: {true_disease:<20} Pred: {pred_disease:<20} Conf: {confidence:.1f}%")

# ==================================================
# SAVE MODEL
# ==================================================
joblib.dump(model, MODEL_PATH)

print("\n" + "="*50)
print(" TRAINING COMPLETE")
print("="*50)
print(" Files created:")
print(f" - Model:           {MODEL_PATH}")
print(f" - Label encoder:   {ENCODER_PATH}")
print(f" - Symptom columns: {SYMPTOM_COLS_PATH}")
print(f" - Symptoms list:   {SYMPTOMS_TXT_PATH}")
print(f" - Total symptoms:  {len(X.columns)}")
print(f" - Diseases:        {len(label_encoder.classes_)}")

# ==================================================
# TEST PREDICTION FUNCTION
# ==================================================
print("\n" + "="*50)
print(" TEST PREDICTION")
print("="*50)

# Test with sample symptoms
test_symptoms = ["chills", "fatigue", "cough", "high_fever", "breathlessness"]
print(f" Testing with symptoms: {test_symptoms}")

# Load model and predict
loaded_model = joblib.load(MODEL_PATH)
X_sample = np.zeros((1, len(X.columns)))

matched_count = 0
for symptom in test_symptoms:
    symptom_clean = clean_symptom(symptom)
    if symptom_clean in X.columns:
        idx = list(X.columns).index(symptom_clean)
        X_sample[0, idx] = 1
        matched_count += 1

print(f" Matched {matched_count}/{len(test_symptoms)} symptoms in the model")

if matched_count > 0:
    probs = loaded_model.predict_proba(X_sample)[0]
    top_idx = np.argsort(probs)[::-1][:5]
    
    print("\n Top 5 Predictions:")
    for i, idx in enumerate(top_idx, 1):
        disease = label_encoder.inverse_transform([idx])[0]
        confidence = probs[idx] * 100
        # Use ASCII arrow -> instead of Unicode →
        print(f"  {i}. {disease:<25} -> {confidence:.2f}%")
else:
    print(" No symptoms matched in the model")

print("\n Model training completed successfully!")