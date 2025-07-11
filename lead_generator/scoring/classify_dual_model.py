import json
import joblib
from sentence_transformers import SentenceTransformer
import numpy as np

# 1. Cargar modelos y encoder
lr_clf = joblib.load("logistic_model.pkl")
rf_clf = joblib.load("randomforest_model.pkl")
label_encoder = joblib.load("label_encoder.pkl")
embedder = SentenceTransformer('sentence-transformers/paraphrase-MiniLM-L6-v2')

# 2. Cargar dataset de test
with open("bios_filtradas.json", "r", encoding="utf-8") as f:
    dataset = json.load(f)

# 3. Clasificar
for item in dataset:
    bio_text = item.get("bio", "").strip()
    if not bio_text:
        continue
    
    embedding = embedder.encode([bio_text])

    lr_probs = lr_clf.predict_proba(embedding)[0]
    rf_probs = rf_clf.predict_proba(embedding)[0]

    # Promedio simple
    avg_probs = (lr_probs + rf_probs) / 2
    pred_index = np.argmax(avg_probs)
    pred_label = label_encoder.inverse_transform([pred_index])[0]

    # Mostrar
    print(f"\n🔍 Usuario: {item.get('username', 'desconocido')} (ID: {item.get('id', '')})")
    print(f"Bio: {bio_text}")
    print(f"➡️ Categoría predicha (promedio): {pred_label}")
    print("Probabilidades promedio por categoría:")
    for cat, prob in zip(label_encoder.classes_, avg_probs):
        print(f" - {cat}: {prob:.2f}")
