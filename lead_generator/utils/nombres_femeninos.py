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
    "luciana", "tatiana", "tania", "rosita","cynthia","anahi"
]

apodos_femeninos = {
    "maría": ["mary", "maru", "marita"],
    "carmen": ["carmela", "carmu"],
    "josefa": ["pepa"],
    "isabel": ["chabela"],
    "laura": ["lauri"],
    "cristina": ["cristy"],
    "francisca": ["paca", "paquita"],
    "marta": ["martu", "martita"],
    "antonia": ["toñi", "antuca"],
    "dolores": [],
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
    "rocío": ["rochita"],
    "mónica": ["moni", "monita"],
    "alicia": ["lichi"],
    "sonia": ["soni"],
    "sandra": ["sandri"],
    "marina": ["marinita"],
    "susana": ["susi", "susy"],
    "margarita": ["marga", "rita"],
    "yolanda": ["yoli", "yola"],
    "natalia": ["naty"],
    "evangelina": [],
    "claudia": [],
    "esther": [],
    "verónica": [],
    "carla": ["carlita"],
    "sofía": ["sofi",],
    "carolina": [],
    "amparo": ["ampita"],
    "lorena": ["lore"],
    "miriam": [],
    "victoria": ["vicky"],
    "daniela": [],
    "alejandra": [],
    "aurora": ["aurorita"],
    "esperanza": ["esperi"],
    "ainhoa": ["ainhoita"]
}

nombres_ambiguos = {
    "ale", "alej", "andy", "andrea", "cris","gabriela", "gabi", "fer",
    "val", "vale", "valen", "joha", "dani", "car", "jackie",
    "vic", "emma", "ema", "emilia", "emi", "manu","manuel","ana"
    "ani","anita","juli","julia","sil","silvi","mar","ali","tere",
    "teru","pauli","miri","esti","ire","clau","pili","lau","rosa"
    "rosi","rosy","maria","lucia","angela","angie","adriana","adri",
    "ines","fabiana","fabi","ele","isa","caro","carol","vero","veru",
    "ro","pati","aleja","espe","eva","evita","eve","nur","lu","bel","lola", 
    "loli", "sof"
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

palabras_femeninas_ampliadas = {
    # Profesiones típicas o roles femeninos (sin nombres propios)
    "enfermera", "maestra", "profesora", "psicóloga", "secretaria", "modista",
    "estilista", "manicurista", "recepcionista", "costurera", "bibliotecaria",
    "cuidadora", "canguro",

    # Adjetivos usados en perfiles femeninos o marketing personal
    "delicada", "sensible", "amorosa", "elegante", "cariñosa", "creativa", 
    "emprendedora", "independiente", "luchadora", "apasionada", "fiel",
    "leal", "detallista", "simpática", "amable", "soñadora", "optimista",
    "inteligente", "dulce", "reflexiva",

    # Rasgos de personalidad o roles sociales
    "madraza", "jefa", "guerrera", "amiga", "confidente", "compañera", "influencer", "inspiradora",

    # Términos de moda, cultura y estética femenina
    "bohemia", "fashion", "hipster", "chic", "glamour", "toxica"

    # Sustantivos asociados con identidad femenina o feminidad
    "maternidad", "feminidad", "sensualidad", "ternura", "fragilidad",

      # Profesiones o roles típicamente femeninos
    "nurse", "teacher", "babysitter", "caregiver", "hairstylist", "makeupartist",
    "receptionist", "secretary", "fashiondesigner", "stylist", "manicurist",

    # Adjetivos femeninos usados en perfiles
    "sweet", "sensitive", "caring", "elegant", "loving", "loyal", "soft",
    "independent", "strongwoman", "dreamy", "romantic", "gentle", "supportive",
    "creative", "classy", "thoughtful", "delicate", "passionate",

    # Identidad / estética femenina
    "girly", "feminine", "lady", "queen", "diva", "barbie", "cutie", "goddess",
    "bossbabe", "girlboss", "fashionista", "glamorous", "vintagegirl", "baddie",

    # Cultura social / redes
    "influencer", "momlife", "bosslady", "wifelife", "makeuplover", "catmom", "dogmom",

    # Rasgos positivos femeninos
    "empathetic", "intuitive", "nurturing", "kindhearted", "beautifulsoul",

    # Identidad de género / expresión
    "woman", "female", "femme", "transfem", "lesbian", "sapphic",

    # Estilo / actitud
    "boho", "chic", "toxic", "spoiled", "fabulous", "sassy", "sparkly", "wifey"

        # Roles y dinámicas BDSM
    "submissive", "sub", "brat", "bratty", "babygirl", "kitten",
    "little", "princess", "doll", "pet", "slut", "slave", "plaything",
    "goodgirl", "badgirl"
    
    # Kinks y prácticas comunes
    "bdsm", "kink", "bondage", "spanking", "choker", "collar",
    "impactplay", "domsub", "masochist", "masochistic", "painlover",
    "fetish", "roleplay", "submission", "punishment", "aftercare",

    # Estética / Cultura
    "leather", "latex", "lingerie", "heels", "fishnets", "bunny",
    "cumslut", "seductress", "temptress", "vixen", "tease", "sensual",
    "naughty", "kinky", "dirtygirl", "sinner", "taboo"

    # Expresiones de marketing sexual indirecto
    "onlyfans", "spicycontent", "exclusivecontent", "privatecontent", "nsfw",
    "hornybabe", "hotwife", "babeslut", "subenergy", "bratenergy", "cumtoy",
    

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

SET_EMOJIS_FEMENINOS = {
    # Corazones y afecto
    "💖", "💕", "💞", "💓", "💗", "💝", "💘", "❣️", "❤️", "🩷", "🤍","🫶", "🥰", "😍", "😚", "😘", "😻", 

    # Flores y naturaleza
    "🌸", "🌷", "🌹", "🪻", "🌼", "🌻", "💐", "🪷", "🌺",

    # Personas y figuras femeninas
    "👩", "👧", "🧕", "👵", "👱‍♀️", "👩‍🦰", "👩‍🦱", "👩‍🦳", "👩‍🦲",
    "👩‍⚕️", "👩‍🎓", "👩‍🏫", "👩‍⚖️", "👩‍🌾", "👩‍🍳", "👩‍🔧", "👩‍🏭",
    "👩‍💼", "👩‍🔬", "👩‍🎨", "👩‍🚒", "👩‍✈️", "👩‍🚀", "👩‍⚖", "👰‍♀️",
    "🤰", "🤱", "🧘‍♀️", "🧖‍♀️", "🧝‍♀️", "🧚‍♀️", "🧛‍♀️", "🧟‍♀️",

    # Belleza y estética
    "💅", "👗", "👠", "👛", "👝", "💄", "👒", "💍", "👙", "👜", "💋",

    # Tiernos, cute, mágicos
    "🧸", "🍼", "👶", "🪄", "🌟", "🌈", "🦋", "🎀",

    # Animales tiernos,
    "🐱", "🐰", "🐶", "🐭", "🐹", "🦄", "🐝", "🐥", "🐣", "🐤", "🐇", "🐈", "🐻‍❄️","🕊️","🐾"

    # Dulces, frutas, estética "kawaii"
    "🍓", "🍒", "🍉", "🍭", "🍬", "🍫", "🍰", "🎂", "🍦", "🧁",
    # Otros
    "🏳️‍🌈"
}

EXPRESIONES_FEMENINAS_BASE = [
    # Reacciones exageradas / emocionales
    "omg", "ohmygod", "me muero", "me morí", "muero de amor", "me vuelvo loca",
    "me mueroooo", "shoro"
    
    # Tiernis / dulces
    "aww", "awww", "cuqui", "cutie", "kawaii", "baby", "bebé", "cosita", "tierna", "tierno",
    "precioso", "preciosa", "hermoso", "hermosa", "divina", "divino", "lindis", "lindooo", "lindaaa",

    # Amorosos / dramáticos
    "te amo", "amoooo", "amol", "te adorooo", "no doy más",
    "estoy llorando", "estoy chillando", "diosss", "dios mío", "ay no", "ay dios", "amo esto",
    
    # Estilo / estética
    "diosa", "queen", "barbie", "princesa", "reina", "fashion", "glam", "bella", "bonita", 
    
]

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
            for bloque in re.findall(r'[a-zA-Z]{3,}', username_limpio):
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

def contiene_emoji_femenino(texto):
    """Detecta si un texto contiene emojis femeninos conocidos o descripciones unicode asociadas a lo femenino."""
    for char in texto:
        if char in SET_EMOJIS_FEMENINOS:
            return True
        nombre_unicode = unicodedata.name(char, "").lower()
        if any(palabra in nombre_unicode for palabra in ["woman", "girl", "female", "princess", "lady"]):
            return True
    return False
from collections import Counter

def contar_emojis_femeninos(texto):
    """Cuenta emojis femeninos con límites por emoji y total."""
    contador = Counter(char for char in texto if char in SET_EMOJIS_FEMENINOS)
    total_emojis = 0
    penalizacion = 0.0
    razones = []

    for emoji, cantidad in contador.items():
        if total_emojis >= 4:
            break
        usados = min(cantidad, 2)
        if usados > 0:
            penalizacion -= 0.2 * usados
            razones.append(f"Emoji femenino '{emoji}' x{usados}")
            total_emojis += 1

    return penalizacion, razones


def es_contenido_femenino(texto):
    """Evalúa si un texto contiene signos de identidad femenina (nombre, palabra o emoji)."""
    texto = normalizar_texto(texto)
    return (
        contiene_nombre_femenino(texto) is True or
        detectar_palabras_femeninas_con_peso(texto) or
        contiene_emoji_femenino(texto)
    )

def detectar_palabras_femeninas_con_peso(texto):
    texto = normalizar_texto(texto or "")
    palabras = set(texto.split())
    penalizacion = 0.0
    razones = []

    # Usamos la lista base + ampliada
    palabras_clave = palabras_femeninas.union(palabras_femeninas_ampliadas)

    for palabra in palabras:
        if palabra in palabras_clave:
            penalizacion -= 0.3
            razones.append(f"Palabra femenina: {palabra}")

    return penalizacion, razones


def es_perfil_de_mujer(username, bio="", comentarios=""):
    username = normalizar_texto(username)
    bio = normalizar_texto(bio)
    comentarios = normalizar_texto(comentarios)

    # Criterios
    if contiene_nombre_femenino(username):
        return True
    if detectar_palabras_femeninas_con_peso(bio):
        return True
    if detectar_palabras_femeninas_con_peso(comentarios):
        return True
    return any(
        es_contenido_femenino(texto)
        for texto in [username, bio, comentarios]
    )

def penalizacion_por_nombre_mujer(username):
    penalizacion = 0.0
    razones = []
    username_norm = normalizar_texto(username)
    username_limpio = re.sub(r'[^a-zA-Z0-9]', '', username_norm)

    for nombre in nombres_descartar:
        nombre_norm = normalizar_texto(nombre)
        if buscar_nombre(nombre_norm, username_norm, username_limpio, nombre_norm in apodos_cortos):
            penalizacion -= 1.0
            razones.append(f"Nombre femenino fuerte detectado: {nombre}")
            return penalizacion, razones  # corto: descarte inmediato

    for nombre in nombres_ambiguos:
        nombre_norm = normalizar_texto(nombre)
        if buscar_nombre(nombre_norm, username_norm, username_limpio):
            penalizacion -= 0.2
            razones.append(f"Nombre ambiguo detectado: {nombre}")
            return penalizacion, razones  # corto: descarte inmediato

    return penalizacion, razones

def penalizacion_por_bio_mujer(bio):
    penalizacion = 0.0
    razones = []

    # Nombre
    if contiene_nombre_femenino(bio) is True:
        penalizacion -= 0.2
        razones.append("Nombre femenino en bio")

    # Palabras
    p_pal, r_pal = detectar_palabras_femeninas_con_peso(bio)
    penalizacion += p_pal
    razones += [r + " en bio" for r in r_pal]

    # Emojis
    p_emo, r_emo = contar_emojis_femeninos(bio)
    penalizacion += p_emo
    razones += [r + " en bio" for r in r_emo]

    return penalizacion, razones


def penalizacion_por_comentario_mujer(comentarios):
    penalizacion = 0.0
    razones = []

    if contiene_nombre_femenino(comentarios) is True:
        penalizacion -= 0.3
        razones.append("Nombre femenino en comentario")

    p_pal, r_pal = detectar_palabras_femeninas_con_peso(comentarios)
    penalizacion += p_pal
    razones += [r + " en comentario" for r in r_pal]

    p_emo, r_emo = contar_emojis_femeninos(comentarios)
    penalizacion += p_emo
    razones += [r + " en comentario" for r in r_emo]

    return penalizacion, razones

def penalizacion_femenina(username="", bio="", comentarios=""):
    return (
        penalizacion_por_nombre_mujer(username) +
        penalizacion_por_bio_mujer(bio) +
        penalizacion_por_comentario_mujer(comentarios)
    )
