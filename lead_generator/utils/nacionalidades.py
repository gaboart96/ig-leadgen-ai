import re
import unicodedata
from .utils import normalizar_texto 

CULTURAS_LENGUAS = {
    # Idiomas principales
    "español": ["es", "español", "castellano", "spanish"],
    "portugués": ["pt", "portugués", "portugues", "português", "portûguês"],
    "inglés": ["en", "inglés", "english"],
    "francés": ["fr", "francés", "francaise", "française", "français"],
    "italiano": ["it", "italiano", "italian"],
    "alemán": ["de", "alemán", "german", "deutsch"],
    "japonés": ["jp", "japonés", "japanese", "日本語"],
    "chino": ["zh", "chino", "mandarín", "chinese", "中文", "汉语", "漢語"],
    "coreano": ["kr", "coreano", "korean", "한국어"],
    "ruso": ["ru", "ruso", "russian", "русский"],
    "árabe": ["ar", "árabe", "arabic", "العربية"],

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
    "Argentina": [
        "Buenos Aires", "CABA", "Capital Federal", "La Plata", "Córdoba", "Mendoza", "Rosario", 
        "Santa Fe", "San Juan", "Salta", "Tucumán", "Bariloche", "Neuquén", "Mar del Plata", 
        "Ushuaia", "Chaco", "Corrientes", "Entre Ríos", "San Luis", "Jujuy", "Misiones", 
        "Formosa", "Patagonia", "Tierra del Fuego"
    ],
    "Colombia": [
        "Bogotá", "Medellín", "Cali", "Barranquilla", "Cartagena", "Pereira", "Cúcuta",
        "Santa Marta", "Manizales", "Bucaramanga", "Villavicencio", "Neiva", "Popayán"
    ],
    "México": [
        "Ciudad de México", "CDMX", "Guadalajara", "Monterrey", "Puebla", "Querétaro", "Cancún", 
        "Tijuana", "Mérida", "León", "Chihuahua", "Oaxaca", "Veracruz", "Toluca", "Acapulco", 
        "San Luis Potosí", "Aguascalientes", "Zacatecas", "Baja California"
    ],
    "Chile": [
        "Santiago", "Valparaíso", "Concepción", "Antofagasta", "La Serena", "Temuco",
        "Viña del Mar", "Puerto Montt", "Arica", "Punta Arenas", "Rancagua", "Copiapó"
    ],
    "Perú": [
        "Lima", "Cusco", "Arequipa", "Trujillo", "Piura", "Chiclayo", "Iquitos", 
        "Tacna", "Puno", "Huancayo", "Callao"
    ],
    "Venezuela": [
        "Caracas", "Maracaibo", "Valencia", "Barquisimeto", "Mérida", "Puerto La Cruz", 
        "Maracay", "San Cristóbal"
    ],
    "Uruguay": [
        "Montevideo", "Punta del Este", "Colonia", "Salto", "Paysandú", "Maldonado"
    ],
    "Paraguay": [
        "Asunción", "Ciudad del Este", "Encarnación", "San Lorenzo", "Luque"
    ],
    "Ecuador": [
        "Quito", "Guayaquil", "Cuenca", "Ambato", "Manta", "Loja", "Esmeraldas"
    ],
    "Bolivia": [
        "La Paz", "Santa Cruz", "Cochabamba", "El Alto", "Sucre", "Potosí", "Oruro", "Tarija"
    ],
    "Costa Rica": [
        "San José", "Alajuela", "Heredia", "Cartago", "Limón", "Guanacaste", "Puntarenas"
    ],
    "Guatemala": [
        "Ciudad de Guatemala", "Antigua", "Quetzaltenango", "Escuintla", "Zacapa"
    ],
    "Honduras": [
        "Tegucigalpa", "San Pedro Sula", "La Ceiba", "Comayagua"
    ],
    "Nicaragua": [
        "Managua", "León", "Granada", "Masaya"
    ],
    "El Salvador": [
        "San Salvador", "Santa Ana", "Soyapango", "La Libertad"
    ],
    "Panamá": [
        "Ciudad de Panamá", "Colón", "David", "Chitré"
    ],
    "Cuba": [
        "La Habana", "Santiago de Cuba", "Varadero", "Cienfuegos"
    ],
    "República Dominicana": [
        "Santo Domingo", "Santiago", "Punta Cana", "La Romana"
    ],
    "Puerto Rico": [
        "San Juan", "Ponce", "Mayagüez", "Bayamón"
    ],
    "España": [
        "Madrid", "Barcelona", "Valencia", "Sevilla", "Málaga", "Bilbao", "Zaragoza", 
        "Granada", "Alicante", "San Sebastián", "Tenerife", "Mallorca", "Ibiza"
    ],
    "Estados Unidos": [
        "Nueva York", "Los Ángeles", "Miami", "Chicago", "San Francisco", "Houston", 
        "Dallas", "Atlanta", "Boston", "Las Vegas", "Seattle", "Orlando", "Washington D.C."
    ],
    "Canadá": [
        "Toronto", "Vancouver", "Montreal", "Ottawa", "Calgary", "Québec", "Edmonton"
    ],
    "Reino Unido": [
        "Londres", "Manchester", "Liverpool", "Birmingham", "Edimburgo", "Glasgow", "Oxford"
    ],
    "Francia": [
        "París", "Marsella", "Lyon", "Niza", "Toulouse", "Burdeos", "Estrasburgo"
    ],
    "Italia": [
        "Roma", "Milán", "Nápoles", "Florencia", "Turín", "Venecia", "Bolonia"
    ],
    "Brasil": [
        "São Paulo", "Río de Janeiro", "Belo Horizonte", "Salvador", "Curitiba", "Porto Alegre", "Brasilia"
    ],
    "Alemania": [
        "Berlín", "Múnich", "Hamburgo", "Frankfurt", "Colonia", "Düsseldorf", "Stuttgart"
    ],
    "China": [
        "Pekín", "Beijing", "Shanghái", "Shenzhen", "Hong Kong", "Guangzhou", "Chengdu"
    ],
    "Japón": [
        "Tokio", "Osaka", "Kioto", "Nagoya", "Yokohama", "Sapporo", "Fukuoka"
    ],
    "Corea del Sur": [
        "Seúl", "Busan", "Incheon", "Daegu"
    ],
    "India": [
        "Nueva Delhi", "Mumbai", "Bangalore", "Chennai", "Hyderabad", "Kolkata"
    ],
    "Turquía": [
        "Estambul", "Ankara", "Antalya", "Izmir"
    ],
    "Emiratos Árabes Unidos": [
        "Dubái", "Abu Dabi", "Sharjah"
    ]
}

def detectar_geolocalizacion_en_bio(bio):
    bio_norm = normalizar_texto(bio.lower())
    bio_original = bio  # Para emojis o mayúsculas

    resultado = {
        "localizaciones": [],
        "culturas_lenguas": [],
    }

    # Detectar menciones culturales o lingüísticas (incluye países)
    for cultura, palabras in CULTURAS_LENGUAS.items():
        for palabra in palabras:
            palabra_normalizada = normalizar_texto(palabra.lower())
            if palabra_normalizada in bio_norm or palabra in bio_original:
                resultado["culturas_lenguas"].append(cultura)
                break  # Evita agregar duplicado por múltiples variantes

    # Detectar localizaciones por país o ciudad
    for pais, ciudades in LOCALIZACION.items():
        if normalizar_texto(pais.lower()) in bio_norm or pais in bio_original:
            resultado["localizaciones"].append(pais)
        for ciudad in ciudades:
            if normalizar_texto(ciudad.lower()) in bio_norm or ciudad in bio_original:
                resultado["localizaciones"].append(ciudad)

    # Quitar duplicados
    resultado["culturas_lenguas"] = list(set(resultado["culturas_lenguas"]))
    resultado["localizaciones"] = list(set(resultado["localizaciones"]))

    return resultado