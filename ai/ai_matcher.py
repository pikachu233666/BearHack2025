import json
import os
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from pathlib import Path

DATASET_PATH = Path("ai/log_samples.json")
LEARN_BUFFER = Path("ai/learn_buffer.json")

# === LOAD DATA ===
with open(DATASET_PATH, "r") as f:
    samples = json.load(f)

logs = [entry["log"] for entry in samples]
actions = [entry["action"] for entry in samples]

# === PREPROCESS ===
def clean_text(text):
    text = text.lower()
    text = re.sub(r"[^\w\s]", "", text)  # remove punctuation
    return text.strip()

cleaned_logs = [clean_text(log) for log in logs]

# === VECTORIZE ===
vectorizer = TfidfVectorizer(stop_words="english")
X = vectorizer.fit_transform(cleaned_logs)

# === MATCH FUNCTION ===
def match_log(log_line):
    cleaned = clean_text(log_line)
    log_vec = vectorizer.transform([cleaned])
    similarities = cosine_similarity(log_vec, X)[0]

    best_score = max(similarities)
    best_index = similarities.argmax()

    if best_score >= 0.7:
        confidence = "high"
        return actions[best_index], best_score, confidence

    elif 0.5 <= best_score < 0.7:
        confidence = "medium"
        return actions[best_index], best_score, confidence

    else:
        # Log this log line to a learning buffer for future improvement
        save_unmatched_log(log_line, best_score)
        return "unknown", best_score, "low"

# === SAVE UNMATCHED LOGS ===
def save_unmatched_log(log_line, score):
    log_entry = {"log": log_line.strip(), "score": round(score, 3)}
    buffer = []

    if LEARN_BUFFER.exists():
        with open(LEARN_BUFFER, "r") as f:
            buffer = json.load(f)

    buffer.append(log_entry)

    with open(LEARN_BUFFER, "w") as f:
        json.dump(buffer, f, indent=2)

def retrain_model():
    global X, actions, logs, vectorizer
    with open(DATASET_PATH, "r") as f:
        samples = json.load(f)

    logs = [clean_text(entry["log"]) for entry in samples]
    actions = [entry["action"] for entry in samples]
    vectorizer = TfidfVectorizer(stop_words="english")
    X = vectorizer.fit_transform(logs)
