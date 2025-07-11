import re
from datetime import datetime

def detectar_edad_o_fecha(bio: str) -> tuple[int | None, str | None]:
    """
    Detecta edad directamente o mediante año de nacimiento.
    Devuelve: (edad estimada, coincidencia encontrada)
    """
    if not bio:
        return None, None

    bio = bio.lower()
    año_actual = datetime.now().year

    # 🧠 Edad explícita
    patrones_edad = [
        r"(\d{1,2})\s*años?",
        r"tengo\s+(\d{1,2})",
        r"(\d{1,2})\s*yo\b",
        r"edad\s*[:\-]?\s*(\d{1,2})",
        r"\b(\d{1,2})\s*y/o\b"
    ]

    for patron in patrones_edad:
        match = re.search(patron, bio)
        if match:
            try:
                edad = int(match.group(1))
                if 12 <= edad <= 80:
                    return edad, match.group(0)
            except:
                continue

    # 📅 Año de nacimiento
    patrones_fecha = [
        r"nacid[ao]\s+en\s+(\d{4})",
        r"born\s+in\s+(\d{4})",
        r"\bb\.?\s*(\d{4})\b",
        r"\bdesde\s+(\d{4})\b",
        r"\b(\d{4})\b"
    ]

    for patron in patrones_fecha:
        match = re.search(patron, bio)
        if match:
            try:
                year = int(match.group(1))
                if 1940 < year <= 2008:
                    edad_estimada = año_actual - year
                    return edad_estimada, match.group(0)
            except:
                continue

    return None, None