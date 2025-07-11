# classify_dataset.py

import json
import joblib
from sentence_transformers import SentenceTransformer
from sklearn.linear_model import LogisticRegression

# Más permisivo (ajusta muy bien training data)
clf = LogisticRegression(C=10, max_iter=1000)

# 1. Cargar modelo, encoder y embedder
clf = joblib.load("classifier_model.pkl")
label_encoder = joblib.load("label_encoder.pkl")
embedder = SentenceTransformer('sentence-transformers/paraphrase-MiniLM-L6-v2')

# 2. Cargar dataset con ids, username y bio
with open("bios_filtradas.json", "r", encoding="utf-8") as f:
    dataset = json.load(f)

# 3. Clasificar usando solo la bio
for item in dataset:
    bio_text = item.get("bio", "").strip()
    if not bio_text:
        continue  # salta si está vacío
    
    embedding = embedder.encode([bio_text])
    pred = clf.predict(embedding)[0]
    probas = clf.predict_proba(embedding)[0]
    
    print(f"\n🔍 Usuario: {item.get('username', 'desconocido')} (ID: {item.get('id', '')})")
    print(f"Bio: {bio_text}")
    print(f"➡️ Categoría predicha: {label_encoder.inverse_transform([pred])[0]}")
    print("Probabilidades por categoría:")
    for cat, prob in zip(label_encoder.classes_, probas):
        print(f" - {cat}: {prob:.2f}")
