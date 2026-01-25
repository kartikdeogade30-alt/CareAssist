import json
import re

# ------------------- LOAD SYMPTOMS -------------------
SYMPTOM_FILE = "data/chat_data/symptoms.json"

with open(SYMPTOM_FILE, "r") as f:
    SYMPTOMS = json.load(f)

# ------------------- NORMALIZATION -------------------
def normalize(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^\w\s]", " ", text)   # remove punctuation
    text = re.sub(r"\s+", " ", text)       # collapse spaces
    return text.strip()

# ------------------- SYMPTOM EXTRACTION -------------------
def extract_symptoms(user_text: str):
    """
    Extract symptoms from free text.
    Works for:
    - skin rash / skin_rash
    - pus filled pimples / pus_filled_pimples
    """

    if not user_text:
        return []

    normalized_text = normalize(user_text)

    found = set()

    for symptom in SYMPTOMS:
        # normalize symptom (underscores → spaces)
        symptom_phrase = normalize(symptom.replace("_", " "))

        # phrase-level match
        if symptom_phrase in normalized_text:
            found.add(symptom)

    return sorted(found)
