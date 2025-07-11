# train_classifier.py

import json
import joblib
from sentence_transformers import SentenceTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report

# 1. Cargar dataset
with open("bios_dataset.json", "r", encoding="utf-8") as f:
    dataset = json.load(f)

bios = [item["bio"] for item in dataset]
categories = [item["categoria"] for item in dataset]

# 2. Embeddings
print("Calculando embeddings...")
embedder = SentenceTransformer('sentence-transformers/paraphrase-MiniLM-L6-v2')
embeddings = embedder.encode(bios)

# 3. Label encoding
label_encoder = LabelEncoder()
labels = label_encoder.fit_transform(categories)

# 4. Entrenamiento
print("Entrenando modelo...")
clf = LogisticRegression(max_iter=1000)
clf.fit(embeddings, labels)

# 5. Guardar
joblib.dump(clf, "classifier_model.pkl")
joblib.dump(label_encoder, "label_encoder.pkl")
print("✅ Modelo y encoder guardados.")

# 6. Evaluación rápida
preds = clf.predict(embeddings)
print("\nReporte de clasificación en training:")
print(classification_report(labels, preds, target_names=label_encoder.classes_))