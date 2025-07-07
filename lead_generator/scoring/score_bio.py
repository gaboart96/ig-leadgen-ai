from sentence_transformers import SentenceTransformer
from sklearn.linear_model import LogisticRegression
from spellchecker import SpellChecker
import numpy as np
import joblib

# 1. Cargar modelo de embeddings
embedder = SentenceTransformer('sentence-transformers/paraphrase-MiniLM-L6-v2')

# 2. Cargar clasificadores entrenados o usar lógica de scoring dummy
# Suponemos que tenés uno por cada factor
# Si aún no los entrenaste, podés simularlos con reglas simples
# clf_seduccion = joblib.load("clasificador_seduccion.pkl")  ← para cuando lo tengas entrenado

# 3. SpellChecker para penalizar errores ortográficos
spell = SpellChecker(language='es')

# 4. Función para puntuar errores ortográficos
def score_ortografia(texto):
    palabras = texto.lower().split()
    errores = spell.unknown(palabras)
    proporcion_error = len(errores) / max(len(palabras), 1)
    return 1.0 - min(proporcion_error * 2, 1.0)  # Penaliza duro si hay muchos errores

# 5. Función principal de análisis de bio
def analizar_bio(bio_text):
    bio = bio_text.strip()
    embedding = embedder.encode([bio])[0]

    # Si tenés clasificadores entrenados, usalos así:
    # score_seduccion = clf_seduccion.predict_proba([embedding])[0][1]

    # Para este ejemplo: scoring con reglas dummy (basado en keywords y embedding)
    seduccion_keywords = ['coach', 'seducción', 'galán', 'ligue', 'pick up']
    fisico_keywords = ['fitness', 'gym', 'mma', 'entrenamiento', 'gimnasio']
    masculina_keywords = ['guerra', 'disciplina', 'lider', 'CEO', 'boxeo', 'fuerza']

    score = lambda kws: min(1.0, sum(k in bio.lower() for k in kws) / len(kws))

    scores = {
        "interes_seduccion": score(seduccion_keywords),
        "enfoque_fisico": score(fisico_keywords),
        "energia_masculina": score(masculina_keywords),
        "status_socioeconomico_cultural": float(any(k in bio.lower() for k in ['abogado', 'ingeniero', 'CEO', 'empresario'])),
        "espiritualidad_fe": float(any(k in bio.lower() for k in ['dios', 'jesus', 'cristiano', 'biblia'])),
        "factor_borrego": float(any(k in bio.lower() for k in ['escorpio', 'river', 'boca', 'kirchnerista', 'libertario'])) + \
                          float(any(e in bio for e in ['🐶', '🐱', '🦮', '🐕', '🐾'])) + \
                          float(sum(c in bio for c in '🔥💯✨❤️🖤') > 2),
        "factor_nerd": float(any(k in bio.lower() for k in ['ajedrez', 'programador', 'desarrollador', 'anime', 'otaku', 'matemáticas', 'código'])) + \
                       float(any('⛩' in bio or '🎮' in bio for c in bio)),
        "score_ortografia": score_ortografia(bio),
    }

    # Normalizamos borrego y nerd (pueden sumar de más)
    scores['factor_borrego'] = min(scores['factor_borrego'], 1.0)
    scores['factor_nerd'] = min(scores['factor_nerd'], 1.0)

    # 6. Score global (suma ponderada simple, ajustable)
    pesos = {
        "interes_seduccion": 0.25,
        "enfoque_fisico": 0.2,
        "energia_masculina": 0.2,
        "status_socioeconomico_cultural": 0.15,
        "espiritualidad_fe": 0.05,
        "factor_borrego": -0.2,
        "factor_nerd": 0.05,
        "score_ortografia": 0.15
    }

    score_global = sum(scores[k] * pesos[k] for k in pesos)

    return {
        "bio": bio_text,
        "scores": scores,
        "score_global": round(score_global, 3)
    }

def scorear_bio(bio_texto):
    resultado = analizar_bio(bio_texto)
    return resultado["score_global"]