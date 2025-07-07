def scorear_fotos_por_carpeta(carpeta_path):
    # Esto lo tenés que implementar si no está aún
    # Por ahora, un dummy que devuelve 0.8 si hay fotos
    import os
    if not os.path.exists(carpeta_path):
        return 0.0
    archivos = os.listdir(carpeta_path)
    if not archivos:
        return 0.0
    return min(1.0, len(archivos) / 10)  # Máximo score si hay 10 o más fotos

def scorear_usuario_global(row):
    """
    row: diccionario con al menos:
        - score_bio
        - score_fotos
        - score_username (opcional)
        - score_comentario (opcional)
    """
    pesos = {
        "score_bio": 0.4,
        "score_fotos": 0.4,
        "score_username": 0.1,
        "score_comentario": 0.1
    }

    score = 0.0
    total_pesos = 0.0
    for key, peso in pesos.items():
        valor = row.get(key)
        if valor is not None:
            score += peso * valor
            total_pesos += peso

    if total_pesos == 0:
        return 0.0

    return round(score / total_pesos, 3)

