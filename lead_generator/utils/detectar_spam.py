import re
import unicodedata
from .utils import normalizar_texto

import re
import unicodedata
from .utils import normalizar_texto

import re
import unicodedata
from .utils import normalizar_texto

def es_spam(usuario, comentario, debug=True):
    texto = f"{usuario} {comentario}".lower()
    penalizacion = 0.0

    if debug:
        print(f"\n🔍 Evaluando SPAM: '{usuario}' | '{comentario}'")

    patrones_spam = [
        r"gratis", r"follow\s?me", r"sigue\s?me", r"dinero", r"promocion",
        r"bit\.ly", r"http[s]?://", r"t\.me/", r"ven[aí]", r"emprend", r"haz clic",
        r"onlyfans", r"dm me", r"trabaja desde casa", r"invierte", r"crypto",
        r"link en bio", r"xxx"
    ]
    for p in patrones_spam:
        if re.search(p, texto):
            penalizacion -= 0.3
            if debug:
                print(f"⚠️ Patrón spam: '{p}' → -0.3")

    for emoji in ["🔞", "🍑", "💋", "🍆"]:
        if emoji in texto:
            penalizacion -= 0.3
            if debug:
                print(f"⚠️ Emoji negativo {emoji} → -0.3")

    for emoji in ["💰"]:
        if emoji in texto:
            penalizacion -= 0.1
            if debug:
                print(f"⚠️ Emoji ambiguo {emoji} → -0.1")

    if re.search(r'\d{5,}', usuario):
        penalizacion -= 0.2
        if debug:
            print("⚠️ Muchos números → -0.2")

    if re.search(r'[_\-\.]{3,}', usuario):
        penalizacion -= 0.2
        if debug:
            print("⚠️ Caracteres repetidos → -0.2")

    urls = re.findall(r'http[s]?://\S+', texto)
    if len(urls) > 1:
        penalizacion -= 0.3
        if debug:
            print(f"⚠️ Varias URLs ({len(urls)}) → -0.3")

    total_letras = len(re.findall(r'[a-zA-Z]', texto))
    mayusculas = len(re.findall(r'[A-Z]', texto))
    if total_letras > 0 and mayusculas / total_letras > 0.7:
        penalizacion -= 0.2
        if debug:
            print("⚠️ Exceso de mayúsculas → -0.2")

    return penalizacion