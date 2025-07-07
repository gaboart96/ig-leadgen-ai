from .utils import normalizar_texto
import unicodedata
import re

nombres_femeninos = [
    "valentina", "camila", "sofia", "martina", "julieta", "agustina", 
    "micaela", "antonella", "milagros", "rocio", "carla", "natalia",
    "paula", "melina", "florencia", "jazmin", "daniela", "gisela", "noelia",
    "celeste", "marina", "romina", "catalina", "ayelen", "barbara", "veronica",
    "yesica", "fernanda", "patricia", "brenda", "carolina",
    "lorena", "leticia", "malena", "pamela", "lourdes", "cecilia", "elena",
    "sheila", "karina", "victoria", "yanina", "delia", "dalia","melisa", "eliana", 
    "luciana", "tatiana", "tania", "rosita","cynthia"
]

apodos_femeninos = {
    "maría": ["mary", "maru", "marita"],
    "carmen": ["carmela", "carmu"],
    "josefa": ["pepa"],
    "isabel": ["isa", "chabela", "bel"],
    "laura": ["lauri"],
    "cristina": ["cristy"],
    "francisca": ["paca", "paquita"],
    "marta": ["martu", "martita"],
    "antonia": ["toñi", "antuca"],
    "dolores": ["lola", "loli"],
    "lucia": ["lu", "luchi"],
    "sara": ["sarita", "sari"],
    "paula": [],
    "elena": ["leny", "ele"],
    "pilar": ["piluca"],
    "raquel": ["raque", "raqui"],
    "mercedes": ["merche", "meche"],
    "rosario": ["rosi", "chayo"],
    "juana": ["juanita", "juanis"],
    "teresa": [],
    "beatriz": ["bea", "betty"],
    "nuria": ["nuri", "nur"],
    "silvia": [],
    "irene": ["irita"],
    "patricia": ["pati"],
    "andrea": ["drea"],
    "rocío": ["ro", "rochita"],
    "mónica": ["moni", "monita"],
    "alicia": ["lichi"],
    "sonia": ["soni"],
    "sandra": ["sandri"],
    "marina": ["marinita"],
    "susana": ["susi", "susy"],
    "margarita": ["marga", "rita"],
    "yolanda": ["yoli", "yola"],
    "natalia": ["naty"],
    "eva": ["evita", "eve"],
    "claudia": [],
    "esther": [],
    "verónica": ["vero", "veru"],
    "carla": ["carlita"],
    "sofía": ["sofi", "sof"],
    "carolina": ["caro", "carol"],
    "amparo": ["ampita"],
    "lorena": ["lore"],
    "miriam": [],
    "victoria": ["vicky"],
    "daniela": [],
    "alejandra": ["aleja"],
    "aurora": ["aurorita"],
    "esperanza": ["espe", "esperi"],
    "ainhoa": ["ainhoita"]
}

nombres_ambiguos = {
    "ale", "alej", "andy", "andrea", "cris","gabriela", "gabi", "gab", "fer",
    "val", "vale", "valen", "jo", "joha", "dani", "car", "jackie",
    "vic", "emma", "ema", "emilia", "emi", "manu","manuel","ana"
    "ani","anita","juli","julia","sil","silvi","mar","ali","tere",
    "teru","pauli","miri","esti","ire","clau","pili","lau","rosa"
    "rosi","rosy","maria","lucia","angela","angie","adriana","adri",
    "ines","fabiana","fabi"
}

palabras_femeninas = {
    "mamá", "mami", "mamita", "mama",
    "tía", "tia",
    "hermana", "hermanita",
    "abuela", "abuelita",
    "novia", "esposa", "pareja", "compañera",
    "princesa", "reina", "diva", "barbie",
    "nena", "nenita", "chica", "minita", "bebé", "baby", "bby",
    "femenina", "femenino", "fem",
    "mujer", "mujercita", "dama", "señorita", "srta",
    "trans", "transfem", "travesti",  
    "lesbiana", "lesbi", "les", "sáfica",
    "mamichula", "guerrera", "linda", "tierna", "bella", "bonita", "preciosa",
    "hembra", 
    "miss", "ms", "mrs", "lady",
    "noviecita", "chiquita", "doll", "cutie", "kawaii",
    "madre", "madrecita", "jefa", "sirena",
    "fashionista", "coqueta", "glam", "girlboss", "goddess",
    "woman", "female", "girl", "lady", "chick", "babe", "queen"
}

apodos_cortos = [a for a in apodos_femeninos if len(a) <= 3]
nombres_descartar = nombres_femeninos + list(apodos_femeninos.keys())


leet_map = {
    'a': '[a4@]',
    'e': '[e3]',
    'i': '[i1!|]',
    'o': '[o0]',
    's': '[s5$]',
    'l': '[l1|]',
    't': '[t7+]',
    'b': '[b8]',
    'g': '[g69]',
}

def nombre_a_patron(nombre):
    return ''.join(leet_map.get(c, c) + '+' for c in nombre)

def buscar_nombre(nombre_norm, username_norm, username_limpio, es_apodo_corto=False):
    # 1. Detección leet
    patron_leet = nombre_a_patron(nombre_norm)
    if re.search(patron_leet, username_limpio):
        return "leet"

    # 2. Si es apodo corto, buscar solo si está separado o tiene vocales repetidas
    if es_apodo_corto:
        patron_apodo = rf'[^a-zA-Z0-9]{nombre_norm}[^a-zA-Z0-9]|{nombre_norm}[aeiou]+'
        if re.search(patron_apodo, username_norm):
            return "apodo separado/repetido"
    else:
        # 3. Nombre embebido en string largo
        if nombre_norm in username_limpio:
            for bloque in re.findall(r'[a-zA-Z]{6,}', username_limpio):
                if nombre_norm in bloque:
                    return "embebido en string largo"

        # 4. Nombre con separadores o vocales extra
        patron_relajado = rf'[^a-zA-Z0-9]*{nombre_norm}[aeiou]*[^a-zA-Z0-9]*'
        if re.search(patron_relajado, username_norm):
            return "separadores o vocales extra"

    return None

def contiene_nombre_femenino(username):
    username_norm = normalizar_texto(username)
    username_limpio = re.sub(r'[^a-zA-Z0-9]', '', username_norm)

    # 1. Nombres que causan descarte
    for nombre in nombres_descartar:
        nombre_norm = normalizar_texto(nombre)
        motivo = buscar_nombre(nombre_norm, username_norm, username_limpio, nombre_norm in apodos_cortos)
        if motivo:
            return True  # Descartar

    # 2. Nombres ambiguos que penalizan
    for nombre in nombres_ambiguos:
        nombre_norm = normalizar_texto(nombre)
        motivo = buscar_nombre(nombre_norm, username_norm, username_limpio)
        if motivo:
            return "penalizar"

    return False

def es_palabra_femenina(texto):
    if any(palabra in texto for palabra in palabras_femeninas):
        return True
    # Adjetivos o sustantivos terminados en "a" (simples)
    for palabra in texto.split():
        if palabra.endswith("a") and len(palabra) > 3:
            return True
    return False

def es_perfil_de_mujer(username, bio="", comentarios=""):
    username = normalizar_texto(username)
    bio = normalizar_texto(bio)
    comentarios = normalizar_texto(comentarios)

    # Criterios
    if contiene_nombre_femenino(username):
        return True
    if es_palabra_femenina(bio):
        return True
    if es_palabra_femenina(comentarios):
        return True
    return False

def penalizacion_femenina(username, bio="", comentarios=""):
    penalizacion = 0.0

    username_norm = normalizar_texto(username)
    username_limpio = re.sub(r'[^a-zA-Z0-9]', '', username_norm)
    bio_norm = normalizar_texto(bio)
    comentarios_norm = normalizar_texto(comentarios)

    # 1. Penalización fuerte si hay nombres femeninos claros
    for nombre in nombres_descartar:
        nombre_norm = normalizar_texto(nombre)
        motivo = buscar_nombre(nombre_norm, username_norm, username_limpio, nombre_norm in apodos_cortos)
        if motivo:
            penalizacion -= 0.7
            break  # si ya encontró, salta a siguiente criterio

    # 2. Penalización suave si hay nombres ambiguos
    for nombre in nombres_ambiguos:
        nombre_norm = normalizar_texto(nombre)
        motivo = buscar_nombre(nombre_norm, username_norm, username_limpio)
        if motivo:
            penalizacion -= 0.1
            break

    # 3. Palabras femeninas en bio o comentarios
    if es_palabra_femenina(bio_norm):
        penalizacion -= 0.2
    #if es_palabra_femenina(comentarios_norm):
        # penalizacion -= 0.

    return penalizacion
