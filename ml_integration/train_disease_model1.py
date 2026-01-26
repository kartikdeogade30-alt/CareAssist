!pip install -q xgboost joblib

from google.colab import files
uploaded = files.upload()

import numpy as np
import pandas as pd
import joblib
from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, f1_score

from xgboost import XGBClassifier

import warnings
warnings.filterwarnings("ignore")

DATA_PATH = "/content/dataset.csv"
MODEL_DIR = Path("/content/disease_model")
MODEL_DIR.mkdir(parents=True, exist_ok=True)

print("Dataset exists:", Path(DATA_PATH).exists())
print("Model dir exists:", MODEL_DIR.exists())

df = pd.read_csv(DATA_PATH)

for col in df.columns:
    df[col] = df[col].astype(str).str.strip().replace("nan", "")

all_symptoms = sorted(set(df.iloc[:, 1:].values.flatten()))
all_symptoms = [s for s in all_symptoms if s != ""]

X = pd.DataFrame(0, index=df.index, columns=all_symptoms)

for i in range(len(df)):
    for symptom in df.iloc[i, 1:].values:
        if symptom:
            X.loc[i, symptom] = 1

min_occurrence = int(0.03 * len(X))
X = X.loc[:, X.sum(axis=0) >= min_occurrence]

label_encoder = LabelEncoder()
y = label_encoder.fit_transform(df["Disease"])

joblib.dump(label_encoder, MODEL_DIR / "label_encoder.pkl")

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y
)

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

print("Training...")
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

print("Accuracy:", accuracy_score(y_test, y_pred))
print("F1:", f1_score(y_test, y_pred, average="weighted"))

joblib.dump(model, MODEL_DIR / "disease_model.pkl")
joblib.dump(list(X.columns), MODEL_DIR / "symptom_columns.pkl")

with open(MODEL_DIR / "symptoms.txt", "w") as f:
    for s in X.columns:
        f.write(s + "\n")

print("\nFILES CREATED:")
!ls /content/disease_model

from google.colab import files

files.download("/content/disease_model/disease_model.pkl")
files.download("/content/disease_model/label_encoder.pkl")
files.download("/content/disease_model/symptom_columns.pkl")
files.download("/content/disease_model/symptoms.txt")

