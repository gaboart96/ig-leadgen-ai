import json
import joblib
from sentence_transformers import SentenceTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report

# 1. Cargar dataset
with open("bios_filtradas_clasificadas.json", "r", encoding="utf-8") as f:
    dataset = json.load(f)

bios = [item["bio"] for item in dataset]
categories = [item["categoria"] for item in dataset]

# 2. Embeddings
print("Generando embeddings...")
embedder = SentenceTransformer('sentence-transformers/paraphrase-MiniLM-L6-v2')
embeddings = embedder.encode(bios)

# 3. Encode labels
label_encoder = LabelEncoder()
labels = label_encoder.fit_transform(categories)

# 4. Entrenar modelos
print("Entrenando LogisticRegression...")
lr_clf = LogisticRegression(C=10, max_iter=1000)
lr_clf.fit(embeddings, labels)

print("Entrenando RandomForest...")
rf_clf = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42)
rf_clf.fit(embeddings, labels)

# 5. Guardar modelos
joblib.dump(lr_clf, "logistic_model.pkl")
joblib.dump(rf_clf, "randomforest_model.pkl")
joblib.dump(label_encoder, "label_encoder.pkl")
print("✅ Modelos guardados.")

# 6. Report rápido
print("\nReport LogisticRegression:")
print(classification_report(labels, lr_clf.predict(embeddings), target_names=label_encoder.classes_))

print("\nReport RandomForest:")
print(classification_report(labels, rf_clf.predict(embeddings), target_names=label_encoder.classes_))