from clip_interrogator import Interrogator
import os

CI = Interrogator()

# --- Palabras clave por categoría ---
CATEGORIAS = {
    "belleza": {
        "positivas": ["beautiful", "handsome", "good looking", "attractive", "model", "clear skin", "symmetrical", "perfect face", "portrait", "elegant", "groomed", "hot", "aesthetic", "sharp jawline"],
        "negativas": ["ugly", "awkward", "blurry", "distorted", "bad lighting", "messy hair", "low quality", "asymmetrical", "weird face"]
    },
    "fisico": {
        "positivas": ["gym", "muscular", "fit", "training", "athlete", "six pack", "bodybuilder", "biceps", "abs", "lifting", "sweaty", "shirtless"],
        "negativas": ["overweight", "fat", "skinny", "unfit", "slouching", "bad posture"]
    },
    "masculinidad": {
        "positivas": ["man", "male", "beard", "masculine", "strong", "alpha", "businessman", "dominant", "confident", "mature", "leather jacket"],
        "negativas": ["feminine", "effeminate", "weak", "shy"]
    },
    "status": {
        "positivas": ["suit", "business", "office", "corporate", "luxury", "watch", "car", "meeting", "conference", "formal attire", "urban background"],
        "negativas": ["casual", "sloppy", "poor", "hoodie", "messy room"]
    },
    "espiritualidad": {
        "positivas": ["church", "prayer", "bible", "faith", "spiritual", "cross", "temple", "god", "religion"],
        "negativas": []
    },
    "borrego": {
        "positivas": ["concert", "crowd", "stadium", "soccer", "match", "audience", "group photo", "team", "beer", "club", "dog", "cat", "selfie", "emoji"],
        "negativas": []
    },
    "nerd": {
        "positivas": ["computer", "coding", "chess", "programmer", "anime", "video game", "manga", "gamer", "books", "glasses", "science", "tech"],
        "negativas": []
    },
    "edad": {
        "positivas": ["young adult", "teenager", "middle aged man", "older man", "elderly"],
        "negativas": []
    }
}

PESOS = {
    "belleza": 0.5,
    "fisico": 1.0,
    "masculinidad": 0.8,
    "status": 1.0,
    "espiritualidad": 0.3,
    "nerd": 0.8,
    "borrego": -0.8,
    "edad": 0.7  # nuevo peso para penalizar extremos
}

# --- Funciones de detección específicas ---
def es_selfie(desc):
    return any(k in desc for k in ["selfie", "mirror selfie", "close-up"])

def es_grupal(desc):
    return any(k in desc for k in ["group of people", "friends", "crowd"])

def es_evento(desc):
    return any(k in desc for k in ["concert", "stadium", "soccer", "match", "audience"])

def calidad_foto(desc):
    if "blurry" in desc or "low quality" in desc:
        return 0.0
    if "high quality" in desc or "professional" in desc:
        return 1.0
    return 0.5

def estimar_edad(desc):
    edades = {
        "teenager": 0.2,
        "young adult": 0.4,
        "middle aged man": 0.6,
        "older man": 0.8,
        "elderly": 1.0
    }
    for k, v in edades.items():
        if k in desc:
            return v
    return 0.5

def ponderar_edad(edad_score):
    distancia = abs(edad_score - 0.4)
    penalizacion = 1 - min(distancia * 2, 1.0)
    return round((1 - distancia) * PESOS["edad"] * penalizacion, 3)

# --- Score por categoría ---
def score_categoria(desc, categoria):
    positivas = CATEGORIAS[categoria]["positivas"]
    negativas = CATEGORIAS[categoria]["negativas"]

    count_pos = sum(k in desc for k in positivas)
    count_neg = sum(k in desc for k in negativas)

    confianza = min(1.0, 0.2 * (count_pos + count_neg))
    bruto = (count_pos * 1.0 - count_neg * 1.0)
    normalizado = max(min(bruto, 3), -3) / 3

    return round(normalizado * confianza, 3)

# --- Evaluación completa de una imagen ---
def evaluar_imagen_clip(path):
    try:
        desc = CI.interrogate(path).lower()

        resultado = {
            "descripcion_clip": desc,
            "es_selfie": es_selfie(desc),
            "es_foto_grupal": es_grupal(desc),
            "es_evento_masivo": es_evento(desc),
            "calidad_foto": calidad_foto(desc),
            "edad_aproximada": estimar_edad(desc)
        }

        score_bruto = 0

        for categoria in CATEGORIAS:
            if categoria == "edad":
                continue
            score_cat = score_categoria(desc, categoria)
            resultado[f"score_{categoria}"] = score_cat

            if categoria in ["belleza", "nerd"]:
                desvio = abs(score_cat - 0.5)
                ajuste = 1 - desvio * 2
                ponderado = round(score_cat * PESOS[categoria] * ajuste, 3)
            else:
                ponderado = round(score_cat * PESOS[categoria], 3)

            resultado[f"ponderado_{categoria}"] = ponderado
            score_bruto += ponderado

        edad_valor = resultado["edad_aproximada"]
        ponderado_edad = ponderar_edad(edad_valor)
        resultado["ponderado_edad"] = ponderado_edad
        score_bruto += ponderado_edad

        resultado["score_total"] = round(score_bruto, 3)
        return resultado

    except Exception as e:
        print(f"⚠️ Error en CLIP: {e}")
        return {
            "descripcion_clip": None,
            "es_selfie": False,
            "es_foto_grupal": False,
            "es_evento_masivo": False,
            "calidad_foto": 0,
            "edad_aproximada": 0.5,
            **{f"score_{cat}": 0 for cat in CATEGORIAS if cat != "edad"},
            **{f"ponderado_{cat}": 0 for cat in CATEGORIAS if cat != "edad"},
            "ponderado_edad": 0,
            "score_total": 0
        }

# --- Evaluación promedio de un perfil (lista de imágenes) ---
def score_clip_perfil(paths):
    resultados = [evaluar_imagen_clip(p) for p in paths if os.path.exists(p)]
    if not resultados:
        return {}

    promedio = {}
    keys = [k for k in resultados[0].keys() if k != "descripcion_clip"]
    for key in keys:
        valores = [r[key] for r in resultados if isinstance(r[key], (int, float))]
        if valores:
            promedio[key] = round(sum(valores) / len(valores), 3)
        else:
            valores_bool = [float(r[key]) for r in resultados if isinstance(r[key], bool)]
            if valores_bool:
                promedio[key] = round(sum(valores_bool) / len(valores_bool), 3)
            else:
                promedio[key] = 0.0

    return promedio


