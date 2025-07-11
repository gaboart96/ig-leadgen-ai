import unicodedata
import re
from urllib.parse import urlparse, parse_qs, unquote

abreviaciones_profesionales = {
    "ing", "dra", "dr", "lic", "arq", "prof", "tec", "abog", "med", "psic", "bioq"
}

def detectar_nombre_punteado(texto):
    palabras = texto.split()
    for palabra in palabras:
        letras = palabra.split(".")
        letras = [l for l in letras if l]  # saca vacíos como en "m.a.r.i.a."

        if len(letras) >= 3 and all(len(l) == 1 for l in letras):  # patrón de iniciales
            reconstruido = ''.join(letras)
            if reconstruido not in abreviaciones_profesionales:
                if contiene_nombre_femenino(reconstruido) is True:
                    return True, f"Nombre punteado detectado: {palabra} → {reconstruido}"
    return False, ""

def normalizar_texto(texto):
    """
    Normaliza un texto para facilitar comparaciones:
    - Pasa a minúsculas
    - Elimina tildes y signos diacríticos
    - Conserva letras, números, espacios y emojis
    - Elimina símbolos de puntuación y caracteres raros

    Ideal para detección de culturas, localizaciones, nombres, etc.
    """
    if not texto:
        return ""

    # Pasa a minúsculas
    texto = texto.lower()

    # Normaliza para separar letras y tildes (e.g. á -> a +  ́)
    texto = unicodedata.normalize('NFD', texto)

    # Elimina los signos diacríticos (categoría Unicode 'Mn')
    texto = ''.join(c for c in texto if unicodedata.category(c) != 'Mn')

    # Elimina todo lo que no sea letra, número, espacio o emoji común
    texto = re.sub(
        r"[^\w\s"
        r"\U0001F600-\U0001F64F"  # Emoticonos
        r"\U0001F300-\U0001F5FF"  # Símbolos y pictogramas
        r"\U0001F680-\U0001F6FF"  # Transporte y mapas
        r"\U0001F1E6-\U0001F1FF"  # Banderas (letras regionales)
        r"]+",
        "",
        texto
    )

    return texto.strip()

"""""

def contiene_nombre_exacto(username, nombres_lista):
    
    username = normalizar_texto(username)
    for nombre in nombres_lista:
        nombre = normalizar_texto(nombre)
        if nombre in username:
            resto = username.replace(nombre, '')
            if not resto or all(c in nombre for c in resto):
                return True
    return False
"""""


def extraer_link_real(instagram_link):
    """
    Extrae el link real del redireccionamiento de Instagram (param 'u')
    """
    parsed_url = urlparse(instagram_link)
    query_params = parse_qs(parsed_url.query)
    if 'u' in query_params:
        return unquote(query_params['u'][0])  # decodifica %3A → :
    return instagram_link  # si no tiene 'u', devuelve el original

def convertir_a_numero(cadena):
    """Convierte texto tipo '2k' o '1.5m' a número entero."""
    try:
        cadena = cadena.lower().replace(',', '').strip()
        if 'k' in cadena:
            return int(float(cadena.replace('k', '')) * 1_000)
        elif 'm' in cadena:
            return int(float(cadena.replace('m', '')) * 1_000_000)
        else:
            return int(cadena)
    except:
        return 0

def parsear_km(valor):
    valor = valor.lower().replace(",", ".")
    if "k" in valor:
        return int(float(valor.replace("k", "")) * 1000)
    elif "m" in valor:
        return int(float(valor.replace("m", "")) * 1_000_000)
    return int(valor)

def obtener_margen_bottom(driver, elemento):
    """Obtiene el margen inferior de un elemento en px (float)."""
    return driver.execute_script("""
        const style = window.getComputedStyle(arguments[0]);
        return parseFloat(style.marginBottom);
    """, elemento)

def es_fecha(texto: str) -> bool:
    """
    Detecta si un texto representa una fecha o marca temporal común en redes sociales.
    """
    if not texto or len(texto) > 50:
        return False

    texto = texto.lower().strip()

    patrones = [
        r"\b\d{1,2}/\d{1,2}/\d{2,4}\b",        # Formatos tipo 12/04/2024
        r"\b\d{1,2}-\d{1,2}-\d{2,4}\b",        # 12-04-2024
        r"\b\d{4}-\d{2}-\d{2}\b",              # 2024-04-12
        r"\b\d{1,2}\s+(de)?\s*[a-záéíóú]+",    # 5 de mayo, 12 enero
        r"\b(hace\s+)?\d+\s*(min|h|d|w|sem|semanas|mes|meses|a|años|años?)\b",  # hace 3 días, 2w, 1a, etc.
        r"\bayer\b", r"\bhoy\b", r"\bmañana\b",
    ]

    for patron in patrones:
        if re.search(patron, texto):
            return True
    return False

def parse_num(texto: str) -> int:
    """
    Parsea números escritos en distintos formatos comunes en redes sociales
    como "1.2k", "3 millones", "1,2 mil", etc. y los convierte en enteros.

    Ejemplos:
        "1.234" → 1234
        "1,2 mil" → 1200
        "2.5k" → 2500
        "3 millones" → 3000000
        "12k seguidores" → 12000
    """
    if not texto:
        return 0

    texto = texto.lower().replace(",", ".")
    texto = texto.strip()

    # Extraer el número flotante inicial
    match = re.search(r"([\d\.]+)", texto)
    if not match:
        return 0

    num = float(match.group(1))

    if "k" in texto or "mil" in texto:
        return int(num * 1_000)
    elif "m" in texto and not "mil" in texto:
        return int(num * 1_000_000)
    elif "millón" in texto or "millones" in texto:
        return int(num * 1_000_000)
    else:
        return int(num)
