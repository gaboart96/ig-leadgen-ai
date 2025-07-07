from deepface import DeepFace
import numpy as np

def analizar_imagen(path):
    try:
        analisis = DeepFace.analyze(
            img_path=path,
            actions=['gender', 'age', 'emotion'],
            enforce_detection=False,
            detector_backend='retinaface'
        )
        if isinstance(analisis, list):
            analisis = analisis[0]
        return analisis
    except Exception as e:
        print(f"⚠️ Error analizando {path}: {e}")
        return None

def score_deepface_perfil(paths):
    total_score = 0
    total_conf = 0
    edades = []
    mujer_score = 0
    usadas = 0

    for path in paths:
        resultado = analizar_imagen(path)
        if not resultado or resultado.get("face_confidence", 0) < 0.5:
            continue

        conf = resultado["face_confidence"]
        edad = resultado["age"]
        mujer_pct = resultado["gender"].get("Woman", 0)
        emocion = resultado["emotion"]

        edades.append(edad)
        mujer_score += mujer_pct / 100

        score = 0
        if emocion.get("happy", 0) > 50:
            score += 0.5
        elif emocion.get("angry", 0) > 30:
            score -= 0.5

        total_score += score * conf
        total_conf += conf
        usadas += 1

    edad_prom = np.mean(edades) if edades else None
    score_final = total_score / total_conf if total_conf else 0

    return {
        "score": score_final,
        "edad_estimada": edad_prom,
        "score_mujer": mujer_score,
        "imagenes_utilizadas": usadas
    }