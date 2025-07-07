from lead_generator.utils import (
    usuario_ya_filtrado,
    usuario_descartado,
    detectar_spam,
    es_perfil_de_mujer,
    PROFESIONES_CLAVE,
    detectar_geolocalizacion_en_bio,
    penalizacion_femenina,
    es_spam
)

def extraer_profesion_por_keywords(bio: str):
    bio = bio.lower()
    for palabra, profesion in PROFESIONES_CLAVE.items():
        if palabra in bio:
            return profesion
    return None

def penalizacion_perfil(publicaciones, seguidores, seguidos, es_privado):
    penalizacion = 0
    if publicaciones < 5:
        penalizacion += 0.2
    if seguidores < 50:
        penalizacion += 0.2
    if seguidores > 0 and seguidos / seguidores > 2:
        penalizacion += 0.2
    if es_privado:
        penalizacion += 0.2
    return min(penalizacion, 1.0)

def filtrar_perfil_por_datos(datos):
    score = datos.get("score_prefiltrado", 0.0)  # arranca desde penalización previa
    razones = []

    print(f"🔍 Calculando score prefiltrado...")
    print(f"📊 Datos: publicaciones={datos.get('publicaciones')}, seguidores={datos.get('seguidores')}, seguidos={datos.get('seguidos')}, historias={datos.get('historias_destacadas')}, bio='{datos.get('bio')}'")

    if datos.get("perfil_privado") and datos.get("publicaciones", 0) == 0:
        score -= 1.0
        razones.append("Privado y sin publicaciones")
        print(f" -1.0 → {score}")

    if datos.get("publicaciones", 0) < 3:
        score -= 0.3
        razones.append("Pocas publicaciones")
        print(f" -0.3 → {score}")

    if datos.get("historias_destacadas", 0) == 0:
        score -= 0.2
        razones.append("Sin historias destacadas")
        print(f" -0.2 → {score}")

    if datos.get("seguidores", 0) < 100:
        score -= 0.3
        razones.append("Pocos seguidores")
        print(f" -0.3 → {score}")

    if datos.get("seguidos", 1) > 0 and datos["seguidores"] / datos["seguidos"] < 0.25:
        score -= 0.2
        razones.append("Ratio bajo")
        print(f" -0.2 → {score}")

    # También detecta spam y femenino
    spam_penal = es_spam(datos.get("username", ""), datos.get("bio", "") or "")
    fem_penal = penalizacion_femenina(datos.get("username", ""), datos.get("bio", ""), datos.get("comentarios", ""))

    score += spam_penal
    score += fem_penal

    if spam_penal:
        razones.append(f"Penalización spam: {spam_penal}")
    if fem_penal:
        razones.append(f"Penalización femenino: {fem_penal}")

    profesion = extraer_profesion_por_keywords(datos.get("bio", ""))
    geo = detectar_geolocalizacion_en_bio(datos.get("bio", ""))

    return {
        "score_prefiltrado": score,
        "razones": razones,
        "profesion": profesion,
        "localizaciones": geo.get("localizaciones", []),
        "culturas": geo.get("culturas", [])
    }