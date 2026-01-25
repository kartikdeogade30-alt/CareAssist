import pandas as pd
import json
import os

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_PATH = os.path.join(BASE_DIR, "../data/dataset.csv")
OUTPUT_PATH = os.path.join(BASE_DIR, "../data/symptoms.json")

# Load dataset
df = pd.read_csv(DATASET_PATH)

# Symptom columns (everything except Disease)
symptom_cols = df.columns[1:]

unique_symptoms = set()

for col in symptom_cols:
    values = df[col].dropna().astype(str)
    for v in values:
        v = v.strip()
        if v:
            unique_symptoms.add(v)

# Save to JSON
with open(OUTPUT_PATH, "w") as f:
    json.dump(sorted(unique_symptoms), f, indent=2)

print(f"Extracted {len(unique_symptoms)} unique symptoms")
print(f"Saved to: {OUTPUT_PATH}")
