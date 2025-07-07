import unicodedata
import re

def normalizar_texto(texto):
    if not texto:
        return ""
    original = texto
    texto = texto.lower()
    texto = unicodedata.normalize("NFD", texto).encode("ascii", "ignore").decode("utf-8")
    texto = re.sub(r'[^\w\s]', '', texto)  # elimina todo salvo letras/numeros/espacios
    texto = re.sub(r'\s+', ' ', texto).strip()
    print(f"🔬 Texto original: '{original}' → Normalizado: '{texto}'")
    return texto

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
