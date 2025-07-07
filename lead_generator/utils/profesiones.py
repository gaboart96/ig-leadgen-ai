# utils_profesion.py

from .utils import normalizar_texto

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
  "fotografo": ["fotógrafo", "photographer", "fotógrafo profesional", "fotógrafo freelance"],
  "videografo": ["videógrafo", "videographer", "filmmaker", "videomaker", "criador de vídeos"],
  "ilustrador": ["ilustrador", "illustrator", "artista visual", "concept artist", "diseñador de personajes"],
  "animador": ["animador 2d", "animador 3d", "animator", "motion designer", "motion graphics"],
  "community_manager": ["community manager", "cm", "social media manager", "gestor de redes", "gestor de comunidades", "content manager"],
  "copywriter": ["copywriter", "redactor publicitario", "content writer", "escritor de contenidos", "copy", "redator", "storyteller"],
  "marketing_digital": ["especialista en marketing digital", "digital marketer", "growth hacker", "analista de marketing", "consultor de marketing", "estratega digital"],
  "ux_writer": ["ux writer", "content designer", "redactor ux", "escritor ux", "product content"],
  "productor_audiovisual": ["productor audiovisual", "content producer", "video producer", "criador de conteúdo", "content creator", "creator"],
  "locutor": ["locutor", "voz en off", "voice actor", "narrador", "voice over", "voice talent"],
  "profesor": ["profesor", "docente", "educador", "maestro", "teacher", "instrutor"],
  "coach": ["coach", "mentor", "life coach", "performance coach", "business coach", "trainer", "formador"],
  "psicologo": ["psicólogo", "psychologist", "terapeuta", "psicólogo clínico", "psicóloga", "psicólogo infantil"],
  "medico": ["médico", "doctor", "doctor en medicina", "médico general", "médico clínico", "doutor"],
  "enfermero": ["enfermero", "enfermera", "nurse", "enfermeiro"],
  "abogado": ["abogado", "abogada", "lawyer", "attorney", "advogado", "legal advisor"],
  "contador": ["contador", "accountant", "contador público", "contabilista", "contador certificado"],
  "economista": ["economista", "economist", "analista económico"],
  "traductor": ["traductor", "translator", "intérprete", "lingüista", "traductor técnico"],
  "electricista": ["electricista", "técnico electricista", "electrician", "eletricista"],
  "plomero": ["plomero", "fontanero", "gasista", "encanador"],
  "mecanico": ["mecánico", "mechanic", "mecánico automotriz", "mecânico"],
  "carpintero": ["carpintero", "woodworker", "carpinteiro", "ebanista"],
  "maquillador": ["maquilladora", "makeup artist", "maquillador", "mua", "maquiadora"],
  "peluquero": ["peluquero", "barbero", "hairstylist", "cabeleireiro"],
  "estilista": ["estilista", "stylist", "fashion stylist", "consultor de imagen"],
  "nutricionista": ["nutricionista", "nutritionist", "especialista en nutrición", "nutri"],
  "personal_trainer": ["entrenador personal", "personal trainer", "coach fitness", "personal", "treinador pessoal"],
  "freelancer": ["freelancer", "freelance", "independiente", "autónomo", "self-employed"],
  "emprendedor": ["emprendedor", "entrepreneur", "founder", "startup founder", "empresario", "criador de negócios"],
  "influencer": ["influencer", "influenciador", "creador de contenido", "digital creator", "influenciadora"],
  "estudiante": ["estudiante", "student", "universitario", "aprendiz", "aluno"],
  "artista": ["artista", "artista visual", "pintor", "escultor", "artista plástico"],
  "arquitecto": ["arquitecto", "architect", "arquiteto"],
  "ingeniero": ["ingeniero", "engineer", "engenheiro", "ing."],
  "biologo": ["biólogo", "biologa", "biologist", "biólogo marino", "biólogo molecular"],
  "quimico": ["químico", "chemist", "químico farmacéutico"],
  "fisico": ["físico", "physicist", "científico físico"],
  "matematico": ["matemático", "mathematician"],
  "geologo": ["geólogo", "geologist", "geólogo ambiental"],
  "meteorologo": ["meteorólogo", "climatólogo", "meteorologist"],
  "veterinario": ["veterinario", "vet", "veterinarian", "veterinária"],
  "chef": ["chef", "cocinero", "cook", "cocinera", "cozinheiro", "gastrónomo"],
  "pastelero": ["pastelero", "pastry chef", "repostero", "confectioner"],
  "bartender": ["bartender", "barman", "barmaid", "cantinero", "coctelero"],
  "mozo": ["mozo", "camarero", "mesero", "waiter", "garçom"],
  "chofer": ["chofer", "conductor", "driver", "motorista", "remisero"],
  "piloto": ["piloto", "aviador", "pilot", "piloto comercial"],
  "azafata": ["azafata", "aeromoza", "flight attendant", "tripulante de cabina"],
  "agricultor": ["agricultor", "granjero", "farmer", "fazendeiro", "campesino"],
  "jardinero": ["jardinero", "gardener", "paisajista", "landscaper"],
  "pescador": ["pescador", "fisherman", "pescador artesanal"],
  "militar": ["militar", "soldado", "army", "forças armadas", "infante"],
  "bombero": ["bombero", "firefighter", "fireman", "bombeiro"],
  "policia": ["policía", "policeman", "oficial", "policial"],
  "politico": ["político", "politician", "diputado", "senador", "ministro"],
  "juez": ["juez", "magistrado", "judge", "jueza"],
  "sacerdote": ["sacerdote", "cura", "padre", "priest", "pastor", "pastoral"],
  "monje": ["monje", "monja", "monk", "nun"],
  "actor": ["actor", "actriz", "actress", "intérprete", "ator"],
  "cantante": ["cantante", "singer", "vocalista", "intérprete musical"],
  "bailarin": ["bailarín", "bailarina", "dancer", "dançarino", "coreógrafo"],
  "modelo": ["modelo", "model", "modelo profesional", "maniquí"],
  "youtuber": ["youtuber", "streamer", "influencer", "creador de contenido", "content creator", "criador de conteúdo"],
  "gamer": ["gamer", "jugador profesional", "pro player", "jogador", "esports"],
  "desempleado": ["desempleado", "sin trabajo", "en transición laboral", "buscando oportunidades", "looking for job", "desempregado"]
}

def extraer_profesion_por_keywords(bio):
    if not bio:
        return None

    bio_normalizada = normalizar_texto(bio)
    print(f"🔍 Bio normalizada: '{bio_normalizada}'")

    for profesion in PROFESIONES_CLAVE:
        if profesion in bio_normalizada:
            print(f"✅ Coincidencia: '{profesion}' en '{bio_normalizada}'")
            return profesion

    print("❌ Ninguna coincidencia encontrada.")
    return None