from lead_generator.utils import (
    usuario_ya_filtrado,
    usuario_descartado,
    detectar_spam,
    es_perfil_de_mujer,
    PROFESIONES_CLAVE,
    es_spam,
    extraer_profesion_por_keywords,
    extraer_culturas,
    extraer_localizaciones,
    penalizacion_por_bio_mujer,
    detectar_edad_o_fecha
)
import json

def evaluar_score_malo(datos):
    score = 0.0
    razones = []

    publicaciones = datos.get("publicaciones", 0)
    seguidores = datos.get("seguidores", 0)
    seguidos = datos.get("seguidos", 1)  # evitar división por 0
    es_privado = datos.get("perfil_privado", False)
    historias = datos.get("historias_destacadas", 0)

    if es_privado:
        score -= 0.3
        razones.append("Privado")

    if historias == 0:
        score -= 0.1
        razones.append("Sin historias destacadas")

    # Penalización por pocas publicaciones (escalonada)
    if publicaciones < 4:
        penal_pubs = 0
        umbral = 4
        paso = 1
        penal_por_paso = 0.1

        while publicaciones < umbral:
            penal_pubs += penal_por_paso
            umbral -= paso

        score -= penal_pubs
        razones.append(f"{publicaciones} publicaciones → -{penal_pubs:.1f}")

    # Penalización por pocos seguidores (escalonada)
    if seguidores < 200:
        penal_seguidores = 0
        umbral = 200
        paso = 25
        penal_por_paso = 0.05

        while seguidores < umbral:
            penal_seguidores += penal_por_paso
            umbral -= paso

        score -= penal_seguidores
        razones.append(f"{seguidores} seguidores → -{penal_seguidores:.1f}")

    # Penalización por ratio seguidos / seguidores (escalonada)
    if seguidores > 0:
        ratio = seguidos / seguidores
        if ratio > 2:
            penal_ratio = 0
            umbral = 2
            paso = 1
            penal_por_paso = 0.05

            while ratio > umbral:
                penal_ratio += penal_por_paso
                umbral += paso

            score -= penal_ratio
            razones.append(f"Ratio {ratio:.2f} seguidos/seguidores → -{penal_ratio:.1f}")

    # Penalización por spam
    spam_penal, motivo_spam = es_spam(datos.get("bio", "") or "")
    if spam_penal:
        score += spam_penal  # viene negativo
        razones.append(f"Penalización spam: {motivo_spam}")

    return round(score, 2), razones


def filtrar_perfil_por_datos(datos):
    print(f"🔍 Calculando score prefiltrado...")
    print(f"📊 Datos: publicaciones={datos.get('publicaciones')}, seguidores={datos.get('seguidores')}, seguidos={datos.get('seguidos')}, historias={datos.get('historias_destacadas')}, bio='{datos.get('bio')}'")

    # Calcular score malo y razones usando la función dedicada
    score_malo, razones_malo = evaluar_score_malo(datos)

    score_mujer = 0.0
    razones_mujer = []

    # Penalización femenina (score mujer)
    fem_penal, fem_razones = penalizacion_por_bio_mujer(datos.get("bio", ""))
    if fem_penal:
        score_mujer += fem_penal
        razones_mujer.extend(fem_razones)

    # Extraer info adicional
    profesion = extraer_profesion_por_keywords(datos.get("bio", ""))
    localizaciones = extraer_localizaciones(datos.get("bio", ""))
    culturas = extraer_culturas(datos.get("bio", ""))
    edad, coincidencia_edad = detectar_edad_o_fecha(datos.get("bio", ""))

    if edad and coincidencia_edad:
        edad_completa = f"{edad} años ({coincidencia_edad})"
    elif edad:
        edad_completa = f"{edad} años"
    else:
        edad_completa = ""

    return {
        "score_malo": round(score_malo, 2),
        "score_mujer": round(score_mujer, 2),
        "razones_malo": razones_malo,
        "razones_mujer": razones_mujer,
        "profesion": profesion,
        "localizaciones": localizaciones,
        "culturas": culturas,
        "edad" : edad_completa
    }
