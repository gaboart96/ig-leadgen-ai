from sentence_transformers import SentenceTransformer
from sklearn.linear_model import LogisticRegression
from spellchecker import SpellChecker
import numpy as np
import joblib

# 1. Cargar modelo de embeddings
embedder = SentenceTransformer('sentence-transformers/paraphrase-MiniLM-L6-v2')

# 2. Cargar clasificadores entrenados o usar lógica de scoring dummy
# Suponemos que tenés uno por cada factor
# Si aún no los entrenaste, podés simularlos con reglas simples
# clf_seduccion = joblib.load("clasificador_seduccion.pkl")  ← para cuando lo tengas entrenado

# 3. SpellChecker para penalizar errores ortográficos
spell = SpellChecker(language='es')

# 4. Función para puntuar errores ortográficos
def score_ortografia(texto):
    palabras = texto.lower().split()
    errores = spell.unknown(palabras)
    proporcion_error = len(errores) / max(len(palabras), 1)
    return 1.0 - min(proporcion_error * 2, 1.0)  # Penaliza duro si hay muchos errores

# 5. Función principal de análisis de bio
def analizar_bio(bio_text):
    bio = bio_text.strip()
    embedding = embedder.encode([bio])[0]

    # Si tenés clasificadores entrenados, usalos así:
    # score_seduccion = clf_seduccion.predict_proba([embedding])[0][1]

    # Para este ejemplo: scoring con reglas dummy (basado en keywords y embedding)
    seduccion_keywords = [
        "coach", "seducción", "seduccion", "galán", "galan", "ligue", "pick up",
        "player", "chicas", "mujeres", "dating", "flirtear", "conquistar",
        "citas", "ligar", "romance", "coquetear", "seductor", "casanova",
        "flirt", "love", "sexy", "atracción", "atractivo", "babe", "girls",
        "relaciones", "novia", "novias", "playboy"
        "💋", "😘", "😉", "😏", "❤️", "🔥", "😍", "🥰", "💕", "💞", "💓", "💗",
        "👄", "👙", "🍑", "🍒", "😈"
    ]
    fisico_keywords = [
        "fitness", "gym", "gimnasio", "mma", "entrenamiento", "pesas", "musculación", 
        "calistenia", "culturismo", "crossfit", "cardio", "runner", "atleta",
        "deportista", "pesas libres", "fuerza física", "powerlifting", "bodybuilding",
        "pull ups", "push ups", "squat", "biceps", "triceps", "abdomen", "six pack",
        "definición", "volumen", "entreno", "workout", "rutina", "shred",
         "🏋️", "🏋️‍♂️", "🏋️‍♀️", "💪", "🦵", "⚡", "🏃", "🤸", "⛹️", "🤼", 
        "🥊", "🚴", "🤾", "🤽", "🏄", "🚵"
    ]
    masculina_keywords = [
          # Guerra y combate
        "guerra", "batalla", "combate", "lucha", "pelea", "boxeo", "mma", "artes marciales",
        "espada", "soldado", "militar"

        # Dominación, jerarquía, conquista
        "dominante", "dominar", "conquista", "territorio", "imperio", 
        "rey"

        # Poder, ambición y estatus
        "poder", "fuerza", "ambición", "dinero", "riqueza", "inversiones", 
        "empresario", "accionista", "fundador", "jefe", 
        "líder", "liderazgo", "estratega",

        # Disciplina, rigor, propósito
        "disciplina", "misión", 
        "persistencia", "resiliencia", "entrenamiento", "rutina", "mentalidad fuerte",

        # Metáforas animales
        "lobo", "tigre", "león", "halcón", "águila",

        # Meta-conceptos
        "status", "jerarquía", "competencia", "rango", "alfa", "masculinidad",
        "virilidad","testosterona", "padre",
         "🔥", "🦁", "👑", "⚔️", "🏆", "🚀", "💪", "🥇", "🥊", "🏹", "🛡️",
        "🐅", "🐺", "🦅", "🐃", "📈", "💰", "💼"
    ]
    desarrollo_personal_keywords = [
        "crecimiento personal", "desarrollo personal", "mejor versión", "autoayuda",
        "mindset", "mentalidad", "propósito", "hábitos", "disciplinado", "superación",
        "motivación", "coaching", "coacheo", "lifecoach", "éxito", "success", 
        "metas", "objetivos", "productividad", "ambición", "inspiración",
        "#growth", "#selfgrowth", "#mindset", "#motivación", "#inspiración",
        "📈", "🚀", "💡", "🌟", "✨"
    ]

    status_socioeconomico_cultural_keywords = [
        "abogado", "abogada", "ingeniero", "ingeniera", "arquitecto", "arquitecta",
        "médico", "medico", "doctor", "doctora", "CEO", "empresario", "empresaria",
        "founder", "cofundador", "co-founder", "startup", "director", "gerente",
        "consultor", "consultora", "licenciado", "licenciada", "catedrático",
        "profesor universitario", "inversionista", "trader", "stock trader",
        "banquero", "finanzas",
        "💼", "📈", "💰", "🏢", "🏦", "👔", "📊", "📝"
    ]

    viajes_multiculturalismo_keywords = [
        "viajes", "viajar", "travel", "wanderlust", "aventura", "mochilero",
        "nómada", "nomad", "trip", "explorar", "exploration", "tour", "turismo",
        "globetrotter", "expat", "expatriado", "internacional", "cultural", 
        "🌍", "🌎", "🌏", "✈️", "🗺️",
        "passport", "visa", "airbnb", "couchsurfing", "hostel", "backpacker"
        "🇪🇸 🇧🇷", "🇪🇸 🇫🇷", "🇪🇸 🇮🇹", "🇪🇸 🇺🇸", "🇪🇸 🇩🇪", "🇪🇸 🇬🇧",
        "🇺🇸 🇧🇷", "🇺🇸 🇫🇷", "🇺🇸 🇮🇹", "🇺🇸 🇩🇪", "🇺🇸 🇬🇧",
        "🇧🇷 🇦🇷", "🇧🇷 🇲🇽", "🇧🇷", "🇧🇷 🇵🇹",
        "🇫🇷 🇮🇹", "🇫🇷 🇪🇸", "🇫🇷 🇵🇹", "🇫🇷 🇬🇧",
        "🇮🇹 🇪🇸", "🇮🇹 🇫🇷", "🇮🇹 🇩🇪", "🇮🇹 🇬🇧",
        "🇩🇪 🇪🇸", "🇩🇪 🇧🇷", "🇩🇪 🇫🇷",
        "🇬🇧 🇺🇸", "🇬🇧 🇪🇸", "🇬🇧 🇮🇹",
        "🇺🇸 🇲🇽", "🇺🇸 🇨🇴", "🇺🇸 🇨🇱",
        "🇺🇸 🇦🇷", "🇺🇸 🇵🇪"
    ]

    factor_nerd_keywords = [
        "ajedrez", "programador", "programadora", "desarrollador", "developer",
        "dev", "software engineer", "matemáticas", "matematicas", "código", "codigo",
        "python", "javascript", "c++", "java", "sql", "frontend", "backend",
        "anime", "otaku", "manga", "cosplay", "gamer", "videojuegos", "juegos",
        "gaming", "streamer", "twitch", "discord", "e-sports",
          # Programación / tech
        "💻", "🖥️", "⌨️", "🖱️", "🧑‍💻", "👨‍💻", "👩‍💻", "⚙️", "📟", "📡", "🔌", "🔧", "📁", "📂", "📜",

        # Anime / otaku / manga
        "⛩", "🗾", "🀄", "🎎",

        # Videojuegos / gaming
        "🎮", "🕹️", "👾", "🔫", 

        # Juegos de mesa / rol
        "🧙‍♂️", "🧝‍♂️",

        # Fantasía / magia
        "🔮", "🪄", "🌌", "✨",

        "神", "愛", "死", "夢", "桜", "光", "月", "夜", "星", # kanji japo típicos
        "한", "국", "사", "랑", # coreano (hangul para "amor", "país")
        "中", "国", "龙", "爱" # chino simplificado

    ]

    espiritualidad_fe_keywords = [
        # Religión judeocristiana / islam / judaísmo
        "dios", "jesus", "cristo", "jesucristo", "biblia", "iglesia", 
        "cristiano", "cristiana", "católico", "catolica", "evangelico", "evangélico",
        "faith", "pray", "🙏", "✝️", "cruz", "bendecido", "bendiciones",
        "oración", "rezar", "santo", "espíritu santo", "gloria a dios", "gracias a dios",
        "yahveh", "torá", "shalom", "israel", "judío", "judio", "judaísmo",
        "allah", "quran", "koran", "ramadan", "musulmán", "musulmana", "islam", "ummah",
        "السلام عليكم", "الله أكبر", "✡️", "☦️", "☪️",

        # Estoicismo y filosofía clásica
        "estoico", "estoicismo", "marco aurelio", "séneca", "epicteto",
        "virtud", "virtud estoica", "carácter", "templanza", "sabiduría", "moderación",
        "autocontrol", "serenidad", "fortaleza interior", "valor moral",

        # Filosofía moral / occidental
        "aristóteles", "platón", "sócrates", "filosofía", "ética", "moral",
        "nietzsche", "voluntad de poder",
        "principios éticos", "principios morales",

        # Responsabilidad y deber (conscientious)
        "responsabilidad", "deber", "obligación", "cumplir", "disciplina",
        "esfuerzo", "sacrificio", "autodominio", "consistencia", "persistencia",
        "integridad", "honor", "lealtad", "principios", "valores",
        "familia tradicional", "liderazgo moral", "ser ejemplo", "orden",

        # Moderno conservador
        "jordan peterson", "12 rules", "12 reglas", "masculinidad clásica",
        "rule", "hierarchy", "orden jerárquico", "redpill",
        # Espiritualidad general
        "✝️", "🙏", "☦️", "☪️", "✡️", "🕎", "📿", "🕊️", "⛪", "🕌", "🕍",
        # Luz / guía moral / conciencia
        "🔥",
        # Fortaleza interior / virtud
        "🛡️", "⚔️", "🏆", "👑", "🦁", "💪",
        # Filosofía / sabiduría
        "📜", "📖", 
        # Familia, orden, tradición
        "👨‍👩‍👧‍👦", "👨‍👩‍👦", "👩‍👩‍👧‍👦", "👨‍👨‍👧‍👦",
        # Consistencia, persistencia
        "⏳", "🏅", "🚀"
    ]
    
    factor_borrego_keywords = [
        # Zodiaco
        "escorpio", "tauro", "aries", "géminis", "geminis", "cáncer", "cancer",
        "leo", "virgo", "libra", "sagitario", "capricornio", "acuario", "piscis",
        # Pensamiento mágico
        "mercurio retrógrado", "mercurio retrogrado", "carta natal",
        "astrología", "astrology", "tarot", "oráculo", "horóscopo", "numerología",
        "manifestar", "manifestación", "manifestando", "universo conspira",
        "vibras", "energía", "frecuencia", "cosmos", "reiki", "chakras",
        "brujita", "witch", "moon", "luna llena", "luna nueva", "signo lunar",
        "sanación", "rituales", "cristales", "amatista", "cuarzo"
        # Fútbol
        "river", "boca", "barcelona", "real madrid", "madridista", "culé",
        "messi", "cristiano ronaldo", "ronaldo", "cr7","selección argentina",
        "champions", "libertadores", "bosteros", "gallina", 
        "racing", "san lorenzo", "independiente", "velez",
        "juventus", "inter de miami", "psg", "manchester united", "chelsea",
        "hincha de", "futbolero", 
        "la albiceleste", "força barça", "hala madrid", "aguante"
        # Política populista o polarizante hispano
        "kirchnerista", "peronista", "amlo", "fjv", "fmln", "petista",
        # Más izquierda latinoamericana
        "chavista", "madurista", "castrochavista", "socialismo", "comunismo",
        "lenin", "marx", "marxista", "izquierda unida", "podemos", "psoe",
        "morena", "pt brasil", "lulista", "fernandez", "sandinista", "evista",
        "kirchner", "cfk", "frente amplio", "mas bolivia", "podemita",
        # Música - tribus
        "ricotero", "rolinga", "metalero", "trapero", "cumbiero", "rockero",
        "kpop", "bts", "belieber", "swiftie", "fan de", "fanático de",

        # Frases genéricas de fandom
        "soy fan", "fan de", "amo a", "fanático de"
        # Zodiaco, espiritualidad superficial
        "✨", "🔮", "🌙", "🌜", "🌛", "⭐", "♈", "♉", "♊", "♋", "♌", "♍",
        "♎", "♏", "♐", "♑", "♒", "♓",
        
        # Pensamiento mágico / energía
        "🧿", "🕉️", "🔆", "💫", "🌌"
        
        # Fútbol y banderas para hinchas
        
        # Música - tribus, fandoms
        
        # Gregarismo social
        "🐑", "🐏", "🐐",  # borregos literal
        "❤️", "💖", "💞", "💯" 
        
        # Mascotas "hijos sustitutos"
        "🐶", "🐱", "🐾"
    ]

    mala_salud_keywords = [
        "fumar", "cigarro", "cigarros", "tabaco", "nicotina", "cigarette", 
        "weed", "marihuana", "porro", "joint", "blunt", "420", "high",
        "stoner", "bong", "ganja", "doobie", "humo",
        "gordo", "gordito", "overweight", "fat", "plus size", "obeso",
        "comida", "foodie", "foodporn", "junk food", "pizza lover", "donuts",
        "🍔", "🍕", "🍟", "🌭", "🍩", "🍰", "🍫", "🍻", "🍺", "🥃", "🚬", "💨"
    ]

    factor_beta_keywords = [
        # Estado civil y pareja
        "casado", "casada", "esposo", "esposa", "mi esposa", "mi esposo",
        "marido", "señora", "comprometido", "comprometida", "novio", "novia",
        "en una relación", "pareja de",
        
        # Padres o familias
        "papá de", "papa de", "mamá de", "mama de", "soy padre", "soy madre",
        "familia", "mis hijos", "nuestros hijos", "mamita", "papito",
        # Corazones blandos y tiernos
        "💖", "💕", "💞", "💓", "💗", "💝", "❣️", "💘", "💟",
        # Emojis “femeninos” o familiares
        "👩‍❤️‍👨", "👨‍👩‍👧", "👨‍👩‍👦", "👨‍👩‍👧‍👦", "👩‍👩‍👦", "👨‍👨‍👦",
        # Mascotas (como prolongación de cuidado familiar)
        "🐶", "🐱", "🦮", "🐕", "🐾"
    ]

    scores = {
        "interes_seduccion": score(seduccion_keywords),
        "interes desarrollo personal" : score(desarrollo_personal_keywords),
        "enfoque_fisico": score(fisico_keywords),
        "energia_masculina": score(masculina_keywords),
        "status_socioeconomico_cultural": score(status_socioeconomico_cultural_keywords),
        "espiritualidad_fe": score(espiritualidad_fe_keywords),
        "factor_borrego": float(any(k in bio.lower() for k in ['escorpio', 'river', 'boca', 'kirchnerista', 'libertario'])) + \
                          float(any(e in bio for e in ['🐶', '🐱', '🦮', '🐕', '🐾'])) + \
                          float(sum(c in bio for c in '🔥💯✨❤️🖤') > 2),
        "factor_nerd": float(any(k in bio.lower() for k in ['ajedrez', 'programador', 'desarrollador', 'anime', 'otaku', 'matemáticas', 'código'])) + \
                       float(any('⛩' in bio or '🎮' in bio for c in bio)),
        "score_ortografia": score_ortografia(bio),
    }

    # Normalizamos borrego y nerd (pueden sumar de más)
    scores['factor_borrego'] = min(scores['factor_borrego'], 1.0)
    scores['factor_nerd'] = min(scores['factor_nerd'], 1.0)

    # 6. Score global (suma ponderada simple, ajustable)
    pesos = {
        "interes_seduccion": 0.25,
        "enfoque_fisico": 0.2,
        "energia_masculina": 0.2,
        "status_socioeconomico_cultural": 0.15,
        "espiritualidad_fe": 0.05,
        "factor_borrego": -0.2,
        "factor_nerd": 0.05,
        "score_ortografia": 0.15
    }

    score_global = sum(scores[k] * pesos[k] for k in pesos)

    return {
        "bio": bio_text,
        "scores": scores,
        "score_global": round(score_global, 3)
    }

def scorear_bio(bio_texto):
    resultado = analizar_bio(bio_texto)
    return resultado["score_global"]