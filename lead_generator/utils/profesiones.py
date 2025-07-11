# utils_profesion.py

from .utils import normalizar_texto
import re

PROFESIONES_CLAVE = {
  "programador": ["programador", "developer", "desarrollador", "coder", "dev", "software developer", "full stack developer", "backend developer", "frontend developer", "engenheiro de software", "desarrollador de software", "systems developer", "analista programador", "técnico en sistemas", "freelance developer", "tech lover", "apasionado por la programación"],
  "analista_de_sistemas": ["analista de sistemas", "systems analyst", "business analyst", "analista funcional", "it analyst", "analista de ti"],
  "qa_tester": ["qa tester", "tester", "quality assurance", "analista qa", "sdet", "testador", "bug hunter"],
  "sysadmin": ["sysadmin", "administrador de sistemas", "devops", "it administrator", "network administrator", "administrador de redes", "especialista em redes"],
  "data_analyst": ["analista de datos", "data analyst", "analista bi", "business intelligence analyst", "data cruncher", "analista de dados"],
  "data_scientist": ["científico de datos", "data scientist", "cientista de dados", "ai researcher", "ml engineer", "machine learning expert"],
  "diseñador_grafico": ["diseñador gráfico", "graphic designer", "designer", "visual designer", "artista digital", "creador visual"],
  "diseñador_ux_ui": ["ux designer", "ui designer", "product designer", "diseñador ux", "diseñador ui", "ux/ui", "experience designer", "interface designer"],
  "editor_video": ["editor de video", "video editor", "montajista", "postproductor", "video creator", "editor audiovisual", "editor de conteúdo audiovisual", "videomaker"],
  "fotografo": ["fotógrafo", "photographer", "fotógrafo profesional", "fotógrafo freelance","photography"],
  "videografo": ["videógrafo", "videographer", "filmmaker", "videomaker", "criador de vídeos"],
  "ilustrador": ["ilustrador", "illustrator", "artista visual", "concept artist", "diseñador de personajes"],
  "animador": ["animador 2d", "animador 3d", "animator", "motion designer", "motion graphics"],
  "community_manager": ["community manager", "cm", "social media manager", "gestor de redes", "gestor de comunidades", "content manager"],
  "copywriter": ["copywriter", "redactor publicitario", "content writer", "escritor de contenidos", "copy", "redator", "storyteller"],
  "marketing_digital": ["especialista en marketing digital", "digital marketer", "growth hacker", "analista de marketing", "consultor de marketing", "estratega digital"],
  "ux_writer": ["ux writer", "content designer", "redactor ux", "escritor ux", "product content"],
  "productor_audiovisual": ["productor audiovisual", "content producer", "video producer", "criador de conteúdo", "content creator", "creator"],
  "locutor": ["locutor", "voz en off", "voice actor", "narrador", "voice over", "voice talent"],
  "profesor": ["profesor", "docente", "educador", "maestro", "teacher", "instrutor","docente"],
  "coach": ["coach", "mentor", "life coach", "performance coach", "business coach", "trainer", "formador"],
  "psicologo": ["psicólogo", "psychologist", "terapeuta", "psicólogo clínico", "psicóloga", "psicólogo infantil"],
  "medico": ["médico", "doctor", "doctor en medicina", "médico general", "médico clínico", "doutor","dr"],
  "enfermero": ["enfermero", "enfermera", "nurse", "enfermeiro"],
  "abogado": ["abogado", "abogada", "lawyer", "attorney", "advogado", "legal advisor"],
  "contador": ["contador", "accountant", "contador público", "contabilista", "contador certificado"],
  "economista": ["economista", "economist", "analista económico"],
  "traductor": ["traductor", "translator", "intérprete", "lingüista", "traductor técnico"],
  "electricista": ["electricista", "técnico electricista", "electrician", "eletricista"],
  "plomero": ["plomero", "fontanero", "gasista", "encanador"],
  "mecanico": ["mecánico", "mechanic", "mecánico automotriz", "mecânico"],
  "carpintero": ["carpintero", "woodworker", "carpinteiro", "ebanista"],
  "maquillador": ["maquillador", "makeup artist"],
  "peluquero": ["peluquero", "barbero", "hairstylist", "cabeleireiro"],
  "estilista": ["estilista", "stylist", "fashion stylist", "consultor de imagen"],
  "nutricionista": ["nutricionista", "nutritionist", "especialista en nutrición", "nutri"],
  "personal_trainer": ["entrenador personal", "personal trainer", "coach fitness", "treinador pessoal","trainer", "fitness","wellness"],
  "deportista": [
    # Español
    "deportista", "atleta", "futbolista", "basquetbolista", "boxeador", "peleador", 
    "jugador", "delantero", "defensor", "portero", "volante", "extremo", "corredor", 
    "maratonista", "ciclista", "tenista", "gimnasta", "nadador", "luchador", 
    "karateka", "skater", "surfista", "patinador",

    # Portugués
    "atleta", "jogador", "futebolista", "zagueiro", "goleiro", "meia", "atacante", 
    "nadador", "boxeador", "lutador", "corredor", "ciclista", "maratonista", 
    "surfista", "skatista", "tenista", "ginasta", "patinador",

    # Inglés
    "athlete", "player", "footballer", "soccer player", "basketball player", 
    "boxer", "fighter", "striker", "midfielder", "goalkeeper", "defender", 
    "runner", "marathoner", "cyclist", "tennis player", "gymnast", "swimmer", 
    "wrestler", "karateka", "skater", "surfer", "ice skater", "sprinter"
    ],
  "freelancer": ["freelancer", "freelance", "independiente", "autónomo", "self-employed"],
  "emprendedor": ["emprendedor", "entrepreneur", "founder", "startup founder", "empresario", "criador de negócios","emprendimiento"],
  "influencer": ["influencer", "influenciador", "creador de contenido", "digital creator"],
  "estudiante": ["estudiante", "student", "universitario", "aprendiz", "aluno"],
  "artista": ["artista", "artista visual", "pintor", "escultor", "artista plástico"],
  "arquitecto": ["arquitecto", "architect", "arquiteto","arq"],
  "ingeniero": ["ingeniero", "engineer", "engenheiro", "ing"],
  "biologo": ["biólogo","biologist", "biólogo marino", "biólogo molecular"],
  "quimico": ["químico", "chemist", "químico farmacéutico"],
  "fisico": ["físico", "physicist", "científico físico"],
  "matematico": ["matemático", "mathematician"],
  "geologo": ["geólogo", "geologist", "geólogo ambiental"],
  "meteorologo": ["meteorólogo", "climatólogo", "meteorologist"],
  "veterinario": ["veterinario", "vet", "veterinarian"],
  "chef": ["chef", "cocinero", "cook", "cozinheiro", "gastrónomo"],
  "pastelero": ["pastelero", "pastry chef", "repostero", "confectioner"],
  "bartender": ["bartender", "barman", "barmaid", "cantinero", "coctelero"],
  "mozo": ["mozo", "camarero", "mesero", "waiter", "garçom"],
  "chofer": ["chofer", "conductor", "driver", "motorista", "remisero"],
  "piloto": ["piloto", "aviador", "pilot", "piloto comercial"],
  "azafata": ["azafata", "flight attendant", "tripulante de cabina"],
  "agricultor": ["agricultor", "granjero", "farmer", "fazendeiro", "campesino"],
  "jardinero": ["jardinero", "gardener", "paisajista", "landscaper"],
  "pescador": ["pescador", "fisherman", "pescador artesanal"],
  "militar": ["militar", "soldado", "army", "forças armadas", "infante"],
  "bombero": ["bombero", "firefighter", "fireman", "bombeiro"],
  "policia": ["policía", "policeman", "oficial", "policial"],
  "politico": ["político", "politician", "diputado", "senador", "ministro"],
  "juez": ["juez", "magistrado", "judge"],
  "sacerdote": ["sacerdote", "cura", "padre", "priest", "pastor", "pastoral"],
  "monje": ["monje", "monk"],
  "actor": ["actor","intérprete", "ator"],
  "cantante": ["cantante", "singer", "vocalista", "intérprete musical"],
  "bailarin": ["bailarín", "dancer", "dançarino", "coreógrafo"],
  "modelo": ["modelo", "model", "modelo profesional", "maniquí"],
  "youtuber": ["youtuber", "streamer", "influencer", "creador de contenido", "content creator", "criador de conteúdo"],
  "gamer": ["gamer", "jugador profesional", "pro player", "jogador", "esports"],
  "trader": ["trader", "stock trader", "trading"],
  "cientifico": [],
  "musico": [
    "guitarrista",
    "guitar player",
    "guitarrist",
    "bajista",
    "bass player",
    "bassist",
    "baterista",
    "drummer",
    "percusionista",
    "percussionist",
    "tecladista",
    "keyboardist",
    "pianista",
    "pianist",
    "violinista",
    "violinist",
    "violista",
    "cellista",
    "chelista",
    "cantante",
    "vocalista",
    "singer",
    "vocalist",
    "compositor",
    "composer",
    "letrista",
    "lyricist",
    "productor musical",
    "music producer",
    "beatmaker",
    "dj",
    "disc jockey",
    "trompetista",
    "trumpet player",
    "saxofonista",
    "saxophonist",
    "flautista",
    "flautist",
    "clarinetista",
    "clarinetist",
    "director de orquesta",
    "orchestra conductor",
    "director musical",
    "music director",
    "multiinstrumentista",
    "multi-instrumentalist",
    "arreglista",
    "arranger",
    "ingeniero de sonido",
    "sound engineer",
    "mezclador",
    "mixing engineer",
    "mastering engineer",
    "corista",
    "backing vocalist"
    ],
  "desempleado": ["desempleado", "sin trabajo", "en transición laboral", "buscando oportunidades", "looking for job", "desempregado"]
}

VARIANTES_PROFESION = []
for variantes in PROFESIONES_CLAVE.values():
    VARIANTES_PROFESION.extend(variantes)

def extraer_profesion_por_keywords(bio):
    if not bio:
        return None

    bio_norm = normalizar_texto(bio)  # conserva puntos si querés, o los elimina si te conviene
    print(f"🔍 Bio normalizada: '{bio_norm}'")

    for profesion_canonica, variantes in PROFESIONES_CLAVE.items():
        for variante in variantes:
            patron = rf'\b{re.escape(variante)}\b'
            if re.search(patron, bio_norm):
                print(f"✅ Coincidencia exacta: '{variante}' → {profesion_canonica}")
                return {
                    "profesion": profesion_canonica,
                    "match": variante
                }

    print("❌ Ninguna coincidencia encontrada.")
    return None

