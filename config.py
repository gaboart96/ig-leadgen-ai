import os

# -------------------------
# 📁 BASE DE DIRECTORIOS
# -------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATABASE_DIR = os.path.join(BASE_DIR, "db")         
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
LOGS_DIR = os.path.join(BASE_DIR, "logs")
TEMP_DIR = os.path.join(BASE_DIR, "temp")
INPUT_DIR = os.path.join(BASE_DIR, "input")
MODELS_DIR = os.path.join(BASE_DIR, "models")
IMG_DIR = os.path.join(OUTPUT_DIR, "img")

# -------------------------
# 📄 ARCHIVOS COMUNES
# -------------------------
DB_FILENAME = "leads_AlfaReal.db"
DB_PATH = os.path.join(DATABASE_DIR, DB_FILENAME)
SCRAPED_CSV_PATH = os.path.join(OUTPUT_DIR, "comentarios_scrapeados.csv")

# -------------------------
# ⚙️ PARÁMETROS DE CONFIGURACIÓN
# -------------------------
GUARDAR_EN_DB = True
GUARDAR_EN_CSV = True
MAX_COMENTARIOS_POR_POST = 5000
MAX_POSTS_POR_PERFIL = 100
TIEMPO_ESPERA_ENTRE_SCROLLS = 2  # en segundos

# -------------------------
# 👤 CREDENCIALES (opcional cargar desde .env)
# -------------------------
IG_USER = ""
IG_PASS = ""