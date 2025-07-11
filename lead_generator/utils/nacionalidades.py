import re
import unicodedata
from .utils import normalizar_texto 

CULTURAS_LENGUAS = {
    # Idiomas principales
    "español": ["español", "castellano", "spanish"],
    "portugués": ["portugués", "portugues", "português", "portûguês"],
    "inglés": ["inglés", "english"],
    "francés": ["francés", "francaise", "française", "français"],
    "italiano": ["italiano", "italian"],
    "alemán": ["alemán", "german", "deutsch"],
    "japonés": ["japonés", "japanese", "日本語"],
    "chino": ["chino", "mandarín", "chinese", "中文", "汉语", "漢語"],
    "coreano": ["coreano", "korean", "한국어"],
    "ruso": ["ruso", "russian", "русский"],
    "árabe": ["árabe", "arabic", "العربية"],

    # Países LATAM y Centroamérica
    "argentina": ["argentina", "argentino", "argentinas", "argentinos", "🇦🇷"],
    "colombia": ["colombiana", "colombiano", "colombianas", "colombianos", "🇨🇴"],
    "mexico": ["mexicana", "mexicano", "mexicanas", "mexicanos", "🇲🇽"],
    "chile": ["chilena", "chileno", "chilenas", "chilenos", "🇨🇱"],
    "peru": ["peruana", "peruano", "peruanas", "peruanos", "🇵🇪"],
    "venezuela": ["venezolana", "venezolano", "venezolanas", "venezolanos", "🇻🇪"],
    "uruguay": ["uruguaya", "uruguayo", "uruguayas", "uruguayos", "🇺🇾"],
    "paraguay": ["paraguaya", "paraguayo", "paraguayas", "paraguayos", "🇵🇾"],
    "ecuador": ["ecuatoriana", "ecuatoriano", "ecuatorianas", "ecuatorianos", "🇪🇨"],
    "bolivia": ["boliviana", "boliviano", "bolivianas", "bolivianos", "🇧🇴"],
    "costa rica": ["costarricense", "tico", "tica", "ticos", "ticas", "🇨🇷"],
    "panamá": ["panameña", "panameño", "panameñas", "panameños", "🇵🇦"],
    "nicaragua": ["nicaragüense", "nicas", "🇳🇮"],
    "honduras": ["hondureña", "hondureño", "hondureñas", "hondureños", "🇭🇳"],
    "guatemala": ["guatemalteca", "guatemalteco", "guatemaltecas", "guatemaltecos", "🇬🇹"],
    "el salvador": ["salvadoreña", "salvadoreño", "salvadoreñas", "salvadoreños", "🇸🇻"],
    "república dominicana": ["dominicana", "dominicano", "dominicanas", "dominicanos", "🇩🇴"],
    "cuba": ["cubana", "cubano", "cubanas", "cubanos", "🇨🇺"],
    "puerto rico": ["puertorriqueña", "puertorriqueño", "boricua", "🇵🇷"],
    "brasil": ["brazil", "brasileño", "brasileiro", "🇧🇷"],

    # América del Norte / Otros
    "estados unidos": ["estadounidense", "americano", "americana", "usa", "🇺🇸"],
    "canadá": ["canadiense", "canadian", "🇨🇦"],
    "méxico": ["mexicano", "mexicana", "🇲🇽"],

    # Europa
    "españa": ["española", "español", "españoles", "españolas", "🇪🇸"],
    "alemania": ["alemana", "alemán", "german", "deutsch", "🇩🇪"],
    "italia": ["italiana", "italiano", "italianas", "italianos", "🇮🇹"],
    "francia": ["francesa", "francés", "franceses", "français", "🇫🇷"],
    "reino unido": ["británica", "británico", "británicas", "británicos", "uk", "british", "🇬🇧"],
    "países bajos": ["holandesa", "holandés", "neerlandés", "🇳🇱"],
    "suiza": ["suiza", "suizo", "🇨🇭"],
    "suecia": ["sueca", "sueco", "🇸🇪"],
    "noruega": ["noruega", "noruego", "🇳🇴"],
    "finlandia": ["finlandesa", "finlandés", "🇫🇮"],

    # Asia y destinos turísticos frecuentes
    "japon": ["japonesa", "japonés", "japanese", "🇯🇵"],
    "china": ["china", "chino", "chinese", "🇨🇳"],
    "corea del sur": ["coreana", "coreano", "korean", "🇰🇷"],
    "india": ["india", "indio", "indiana", "🇮🇳"],
    "tailandia": ["tailandesa", "tailandés", "🇹🇭"],
    "indonesia": ["indonesia", "indonesio", "🇮🇩"],
    "filipinas": ["filipina", "filipino", "🇵🇭"],
    "turquía": ["turca", "turco", "turkish", "🇹🇷"],
    "israel": ["israelí", "🇮🇱"],
    "emiratos árabes": ["emiratí", "dubai", "🇦🇪"],

    # África (principales)
    "sudáfrica": ["sudafricana", "sudafricano", "🇿🇦"],
    "egipto": ["egipcia", "egipcio", "🇪🇬"],
    "nigeria": ["nigeriana", "nigeriano", "🇳🇬"],
    "marruecos": ["marroquí", "🇲🇦"]
}

LOCALIZACION = {
  "Argentina": {
    "localizaciones": [
      "Buenos Aires",
      "CABA",
      "Capital Federal",
      "La Plata",
      "Córdoba",
      "Mendoza",
      "Rosario",
      "Santa Fe",
      "San Juan",
      #"Salta",
      "Tucumán",
      "Bariloche",
      "Neuquén",
      "Mar del Plata",
      "Ushuaia",
      "Chaco",
      "Corrientes",
      "Entre Ríos",
      "San Luis",
      "Jujuy",
      "Misiones",
      "Formosa",
      "Patagonia",
      "Tierra del Fuego"
    ],
    "gentilicios": [
      "argentino",
      "argentina",
      "bonaerense",
      "porteño",
      "porteña",
      "platense",
      "cordobés",
      "cordobesa",
      "mendocino",
      "mendocina",
      "rosarino",
      "rosarina",
      "santafesino",
      "santafesina",
      "sanjuanino",
      "salteño",
      "tucumano",
      "barilochense",
      "neuquino",
      "marplatense",
      "ushuaiense",
      "chaqueño",
      "correntino",
      "entrerriano",
      "sanluiseño",
      "jujeño",
      "misionero",
      "formoseño",
      "patagónico",
      "fueguino"
    ]
  },
  "Colombia": {
    "localizaciones": [
      "Bogotá",
      "Medellín",
      "Cali",
      "Barranquilla",
      "Cartagena",
      "Bucaramanga",
      "Cúcuta",
      "Pereira",
      "Manizales",
      "Santa Marta",
      "Ibagué",
      "Villavicencio",
      #"Pasto",
      "Montería",
      "Neiva"
    ],
    "gentilicios": [
      "colombiano",
      "colombiana",
      "bogotano",
      "bogotana",
      "medellinense",
      "caleño",
      "caliño",
      "barranquillero",
      "cartagenero",
      "bucaramangués",
      "cucuteño",
      "pereirano",
      "manizaleño",
      "santamartense",
      "ibaguereño",
      "villavicense",
      "pastoense",
      "monteriano",
      "neivano"
    ]
  },
  "México": {
    "localizaciones": [
      "Ciudad de México",
      "México D.F.",
      "Guadalajara",
      "Monterrey",
      "Puebla",
      "Toluca",
      "Tijuana",
      "León",
      "Querétaro",
      "Mérida",
      "Cancún",
      "Chiapas",
      "Oaxaca",
      "Veracruz"
    ],
    "gentilicios": [
      "mexicano",
      "mexicana",
      "chilango",
      "chilang@",
      "jalisciense",
      "monterreyense",
      "poblano",
      "tolucaño",
      "tijuanense",
      "leonés",
      "queretano",
      "meridano",
      "cancunense",
      "chiapaneco",
      "oaxaqueño",
      "veracruzano"
    ]
  },
  "Chile": {
    "localizaciones": [
      "Santiago de Chile",
      "Valparaíso",
      "Viña del Mar",
      "Concepción",
      "La Serena",
      "Antofagasta",
      "Temuco",
      "Rancagua",
      "Puerto Montt",
      "Punta Arenas"
    ],
    "gentilicios": [
      "chileno",
      "chilena",
      "santiaguino",
      "santiaguina",
      "porteño",
      "porteña",
      "viñamarino",
      "concepcionista",
      "serenense",
      "antofagastino",
      "temucano",
      "rancagüino",
      "puertomontino",
      "puntarenense"
    ]
  },
  "Perú": {
    "localizaciones": [
      "Lima",
      "Cusco",
      "Arequipa",
      "Trujillo",
      "Piura",
      "Chiclayo",
      "Iquitos",
      "Tacna",
      "Puno",
      "Huancayo",
      "Callao"
    ],
    "gentilicios": [
      "peruano",
      "limeño",
      "cusqueño",
      "arequipeño",
      "trujillano",
      "piurano",
      "chiclayano",
      "iquiteño",
      "tacneño",
      "puneño",
      "huancaíno",
      "chalaco"
    ]
  },
  "Venezuela": {
    "localizaciones": [
      "Caracas",
      "Maracaibo",
      "Valencia",
      "Barquisimeto",
      "Mérida",
      "Puerto La Cruz",
      "Maracay",
      "San Cristóbal"
    ],
    "gentilicios": [
      "venezolano",
      "caraqueño",
      "marabino",
      "valenciano",
      "barquisimetano",
      "merideño",
      "porteño",
      "maracayero",
      "sancristobalense"
    ]
  },
  "Uruguay": {
    "localizaciones": [
      "Montevideo",
      "Punta del Este",
      "Colonia",
      "Salto",
      "Paysandú",
      "Maldonado"
    ],
    "gentilicios": [
      "uruguayo",
      "montevideano",
      "puntesteño",
      "coloniense",
      "salteño",
      "paysandúense",
      "maldonadense"
    ]
  },
  "Paraguay": {
    "localizaciones": [
      "Asunción",
      "Ciudad del Este",
      "Encarnación",
      "San Lorenzo",
      "Luque"
    ],
    "gentilicios": [
      "paraguayo",
      "asunceno",
      "esteño",
      "encarnaceno",
      "sanlorenzano",
      "luqueño"
    ]
  },
  "Ecuador": {
    "localizaciones": [
      "Quito",
      "Guayaquil",
      "Cuenca",
      "Ambato",
      "Manta",
      "Loja",
      "Esmeraldas"
    ],
    "gentilicios": [
      "ecuatoriano",
      "quiteño",
      "guayaquileño",
      "cuencano",
      "ambateño",
      "manteño",
      "lojaíno",
      "esmeraldeño"
    ]
  },
  "Bolivia": {
    "localizaciones": [
      "La Paz",
      "Santa Cruz",
      "Cochabamba",
      #"El Alto",
      "Sucre",
      "Potosí",
      "Oruro",
      "Tarija"
    ],
    "gentilicios": [
      "boliviano",
      "paceño",
      "cruceño",
      "cochabambino",
      "alteño",
      "sucrense",
      "potosino",
      "orureño",
      "tarijeño"
    ]
  },
  "Costa Rica": {
    "localizaciones": [
      "San José",
      "Alajuela",
      "Heredia",
      "Cartago",
      #"Limón",
      "Guanacaste",
      "Puntarenas"
    ],
    "gentilicios": [
      "costarricense",
      "tico",
      "josefino",
      "alajuelense",
      "herediano",
      "cartaginés",
      "limonense",
      "guanacasteco",
      "puntarenense"
    ]
  },
  "Guatemala": {
    "localizaciones": [
      "Ciudad de Guatemala",
      "Antigua",
      "Quetzaltenango",
      "Escuintla",
      "Zacapa"
    ],
    "gentilicios": [
      "guatemalteco",
      "chapín",
      "antigüeño",
      "quetzalteco",
      "escuintleco",
      "zacapaneco"
    ]
  },
  "Honduras": {
    "localizaciones": [
      "Tegucigalpa",
      "San Pedro Sula",
      "La Ceiba",
      "Comayagua"
    ],
    "gentilicios": [
      "hondureño",
      "tegucigalpense",
      "sampedrano",
      "ceibeño",
      "comayagüense"
    ]
  },
  "Nicaragua": {
    "localizaciones": [
      "Managua",
      "León",
      "Granada",
      "Masaya"
    ],
    "gentilicios": [
      "nicaragüense",
      "managüense",
      "leonés",
      "granadino",
      "masayense"
    ]
  },
  "El Salvador": {
    "localizaciones": [
      "San Salvador",
      "Santa Ana",
      "Soyapango",
      #"La Libertad"
    ],
    "gentilicios": [
      "salvadoreño",
      "santaneco",
      "soyapaneco",
      "liberteño"
    ]
  },
  "Panamá": {
    "localizaciones": [
      "Ciudad de Panamá",
      #"Colón",
      #"David",
      "Chitré"
    ],
    "gentilicios": [
      "panameño",
      "capitalino",
      "colonense",
      "davideño",
      "chitreano"
    ]
  },
  "Cuba": {
    "localizaciones": [
      "La Habana",
      "Santiago de Cuba",
      "Varadero",
      "Cienfuegos"
    ],
    "gentilicios": [
      "cubano",
      "habanero",
      "santiaguero",
      "varaderense",
      "cienfueguero"
    ]
  },
  "República Dominicana": {
    "localizaciones": [
      "Santo Domingo",
      "Santiago",
      "Punta Cana",
      "La Romana"
    ],
    "gentilicios": [
      "dominicano",
      "santodomingueño",
      "santiaguero",
      "puntacanseño",
      "romano"
    ]
  },
  "Puerto Rico": {
    "localizaciones": [
      "San Juan",
      "Ponce",
      "Mayagüez",
      "Bayamón"
    ],
    "gentilicios": [
      "puertorriqueño",
      "boricua",
      "sanjuanero",
      "ponceño",
      "mayagüezano",
      "bayamonés"
    ]
  },
  "Brasil": {
    "localizaciones": [
      "São Paulo",
      "Río de Janeiro",
      "Belo Horizonte",
      #"Salvador",
      "Curitiba",
      "Porto Alegre",
      "Brasilia"
    ],
    "gentilicios": [
      "brasileño",
      "paulista",
      "carioca",
      "belo-horizontino",
      #"salvadoreño",
      "curitibano",
      "portoalegrense",
      "brasiliense"
    ]
  },
  "Mundo": {
    "localizaciones": [
        "Nueva York",
        "Los Ángeles",
        "Chicago",
        "Toronto",
        "Vancouver",
        "Londres",
        "Manchester",
        "París",
        "Marsella",
        "Berlín",
        "Hamburgo",
        "Roma",
        "Milán",
        "Madrid",
        "Barcelona",
        "Ámsterdam",
        "Bruselas",
        "Moscú",
        "San Petersburgo",
        "El Cairo",
        "Johannesburgo",
        "Nairobi",
        "Lagos",
        "Sídney",
        "Melbourne",
        "Auckland",  # Nueva Zelanda
        "Wellington",
        "Tokio",
        "Osaka",
        "Seúl",
        "Busán",
        "Bangkok",
        "Yakarta",
        "Kuala Lumpur",
        "Singapur",
        "Dubái",
        "Tel Aviv",
        "Estambul",
        "Teherán",
        "Bagdad",
        "Karachi",
        "Bombay",
        "Delhi",
        "Bangalore",
        "Ciudad de México",
        "Guadalajara",
        "Monterrey",
        "Buenos Aires",
        "Santiago",
        "Lima",
        "Bogotá",
        "Caracas",
        "Montevideo",
        "La Habana"
    ],
    "gentilicios": [
        "neoyorquino",
        "angelino",
        "chicaguense",
        "torontés",
        "vancouverense",
        "londinense",
        "manchuniano",
        "parisino",
        "marsellés",
        "berlinés",
        "hamburgués",
        "romano",
        "milanés",
        "madrileño",
        "barcelonés",
        "amsterdamés",
        "bruselense",
        "moscovita",
        "petersburgués",
        "cairino",
        "johannesburgués",
        "naiborense",
        "lagosiano",
        "sídneyense",
        "melburniano",
        "aucklander",  # inglés informal
        "wellingtoniano",
        "tokiano",
        "osakense",
        "seulense",
        "busanés",
        "bangkonés",
        "yakarteño",
        "kuala lumpurense",
        "singapurense",
        "dubaí",
        "telavivense",
        "estambulí",
        "teheraní",
        "bagdadí",
        "karachiano",
        "mumbaikar",  # común en India para Bombay
        "delhiense",
        "bangaloreano",
        "mexicano",
        "tapatío",
        "regiomontano",
        "porteño",
        "santiaguino",
        "limeño",
        "bogotano",
        "caraqueño",
        "montevideano",
        "habanero"
    ]
}
}

def extraer_culturas(bio):
    if not bio:
        return []

    bio_normalizada = normalizar_texto(bio)
    print(f"🌎 Bio para culturas: '{bio_normalizada}'")

    culturas_detectadas = []
    for cultura, variantes in CULTURAS_LENGUAS.items():
        for variante in variantes:
            variante_normalizada = normalizar_texto(variante)
            patron = rf"\b{re.escape(variante_normalizada)}\b"
            if re.search(patron, bio_normalizada):
                print(f"✅ Cultura detectada: {cultura}(\"{variante}\")")
                culturas_detectadas.append(f"{cultura}(\"{variante}\")")
                # break

    return culturas_detectadas

def extraer_localizaciones(bio):
    if not bio:
        return []

    bio_normalizada = normalizar_texto(bio)
    print(f"📍 Bio para localizaciones: '{bio_normalizada}'")

    localizaciones_detectadas = []
    for pais, datos in LOCALIZACION.items():
        for variante in datos["localizaciones"] + datos.get("gentilicios", []):
            variante_normalizada = normalizar_texto(variante)
            patron = rf"\b{re.escape(variante_normalizada)}\b"
            if re.search(patron, bio_normalizada):
                print(f"✅ Localización detectada: {pais}(\"{variante}\")")
                localizaciones_detectadas.append(f"{pais}(\"{variante}\")")
                # break

    return localizaciones_detectadas


def detectar_geolocalizacion_en_bio(bio):
    bio_norm = normalizar_texto(bio.lower())
    bio_original = bio  # Para emojis o mayúsculas

    resultado = {
        "localizaciones": [],
        "culturas_lenguas": [],
    }

    # Detectar menciones culturales o lingüísticas
    for cultura, palabras in CULTURAS_LENGUAS.items():
        for palabra in palabras:
            palabra_normalizada = normalizar_texto(palabra.lower())
            if palabra_normalizada in bio_norm or palabra in bio_original:
                resultado["culturas_lenguas"].append(cultura)
                break

    # Detectar localizaciones por país, ciudad o gentilicio
    for pais, datos in LOCALIZACION.items():
        if normalizar_texto(pais.lower()) in bio_norm or pais in bio_original:
            resultado["localizaciones"].append(pais)

        for ciudad in datos["localizaciones"]:
            if normalizar_texto(ciudad.lower()) in bio_norm or ciudad in bio_original:
                resultado["localizaciones"].append(ciudad)

        for gentilicio in datos.get("gentilicios", []):
            if normalizar_texto(gentilicio.lower()) in bio_norm or gentilicio in bio_original:
                resultado["localizaciones"].append(pais)

    # Quitar duplicados
    resultado["culturas_lenguas"] = list(set(resultado["culturas_lenguas"]))
    resultado["localizaciones"] = list(set(resultado["localizaciones"]))

    return resultado