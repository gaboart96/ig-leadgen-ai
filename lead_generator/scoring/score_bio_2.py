from sentence_transformers import SentenceTransformer
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression
import joblib

model = SentenceTransformer('sentence-transformers/paraphrase-MiniLM-L6-v2')
embeddings = model.encode([item["bio"] for item in dataset])


le = LabelEncoder()
labels = le.fit_transform([item["categoria"] for item in dataset])

clf = LogisticRegression(max_iter=1000)
clf.fit(embeddings, labels)