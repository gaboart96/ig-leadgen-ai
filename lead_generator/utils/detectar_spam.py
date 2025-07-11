import re
import unicodedata
from .utils import normalizar_texto

def contiene_idioma_raro(texto):
    """Detecta si hay caracteres de idiomas poco comunes para spam (hindi, árabe, cirílico, etc.)"""
    penaliza = False
    for char in texto:
        code = ord(char)
        if (
            0x0600 <= code <= 0x06FF   # árabe
            or 0x0900 <= code <= 0x097F  # devanagari (hindi)
            or 0x0400 <= code <= 0x04FF  # cirílico (ruso, ucraniano)
            or 0x0E00 <= code <= 0x0E7F  # tailandés
            or 0x4E00 <= code <= 0x9FFF  # chino / japonés
        ):
            return True
    return False


def es_spam(texto, debug=True):
    texto = texto.lower()
    penalizacion = 0.0
    razones = []

    if debug:
        print(f"\n🔍 Evaluando SPAM: '{texto}'")

    patrones_spam = [
        r"gratis", r"follow\s?me", r"sigue\s?me", r"dinero", r"promocion",
        r"bit\.ly", r"http[s]?://", r"t\.me/", r"ven[aí]", r"emprend", r"haz clic",
        r"onlyfans", r"dm me", r"trabaja desde casa", r"invierte", r"crypto",
        r"link en bio", r"xxx"
    ]
    for p in patrones_spam:
        if re.search(p, texto):
            penalizacion -= 0.3
            razones.append(f"Patrón spam: '{p}' → -0.3")

    for emoji in ["🔞", "🍑", "💋", "🍆"]:
        if emoji in texto:
            penalizacion -= 0.3
            razones.append(f"Emoji negativo {emoji} → -0.3")

    for emoji in ["💰"]:
        if emoji in texto:
            penalizacion -= 0.1
            razones.append(f"Emoji ambiguo {emoji} → -0.1")

    if re.search(r'\d{5,}', texto):
        penalizacion -= 0.2
        razones.append("Muchos números → -0.2")

    if re.search(r'[_\-\.]{3,}', texto):
        penalizacion -= 0.2
        razones.append("Caracteres repetidos → -0.2")

    urls = re.findall(r'http[s]?://\S+', texto)
    if len(urls) > 1:
        penalizacion -= 0.3
        razones.append(f"Varias URLs ({len(urls)}) → -0.3")

    total_letras = len(re.findall(r'[a-zA-Z]', texto))
    mayusculas = len(re.findall(r'[A-Z]', texto))
    if total_letras > 0 and mayusculas / total_letras > 0.7:
        penalizacion -= 0.2
        razones.append("Exceso de mayúsculas → -0.2")

    if contiene_idioma_raro(texto):
        penalizacion -= 0.4
        razones.append("Idioma raro → -0.4")

    return penalizacion, razones