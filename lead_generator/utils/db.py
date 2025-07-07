import sqlite3
import pandas as pd
import os
from os import listdir
from os.path import isfile, join
from config import DB_PATH, DATABASE_DIR, DB_FILENAME
import json

def crear_conexion():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    crear_tablas_si_no_existen(conn)
    return conn


def cerrar_conexion(conn):
    if conn:
        conn.close()

def conectar_db(path):
    return sqlite3.connect(path)

def iniciar_db():
    os.makedirs(DATABASE_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    crear_tablas_si_no_existen(conn)
    return conn

def crear_tablas_si_no_existen(conn):
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios_filtrados (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            comentarios TEXT,
            fotos_analizadas INTEGER,
            fotos_sin_personas INTEGER,
            flag_incompleto BOOLEAN,
            filtro_descartado BOOLEAN,
            motivo_descartado TEXT,
            bio TEXT,
            perfil_privado BOOLEAN,
            publicaciones INTEGER,
            seguidores INTEGER,
            seguidos INTEGER,
            historias_destacadas INTEGER,
            links_externos TEXT,
            edad_estimada REAL,
            profesion_estimada TEXT,
            localizaciones TEXT,
            culturas TEXT,
            score_prefiltrado REAL,          
            score_clip REAL,
            score_deepface REAL,         
            score_final INTEGER          
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS comentarios (
            username TEXT,
            comentario TEXT,
            fecha TEXT,
            post_url TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios_unicos (
            username TEXT PRIMARY KEY,
            comentario1 TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS descartados (
            username TEXT PRIMARY KEY
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS posts_scrapeados (
            url TEXT PRIMARY KEY
        )
    """)

    conn.commit()

def guardar_usuario_filtrado(conn, datos):
    localizaciones_json = json.dumps(datos.get("localizaciones", []))
    culturas_json = json.dumps(datos.get("culturas", []))
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO usuarios_filtrados (
                username, comentarios,
                fotos_analizadas, fotos_sin_personas,
                flag_incompleto, filtro_descartado, motivo_descartado,
                bio, perfil_privado, publicaciones, seguidores, seguidos,
                historias_destacadas, links_externos,
                edad_estimada, profesion_estimada, localizaciones, culturas,
                score_prefiltrado,
                score_clip, score_deepface,
                score_final
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            datos.get("username"),
            datos.get("comentarios"),
            datos.get("fotos_analizadas", 0),
            datos.get("fotos_sin_personas", 0),
            datos.get("flag_incompleto", False),
            datos.get("filtro_descartado", False),
            datos.get("motivo_descartado", ""),
            datos.get("bio", ""),
            datos.get("perfil_privado", False),
            datos.get("publicaciones", 0),
            datos.get("seguidores", 0),
            datos.get("seguidos", 0),
            datos.get("historias_destacadas", 0),
            datos.get("links_externos", ""),
            datos.get("edad_estimada"),
            datos.get("profesion_estimada"),
            localizaciones_json,
            culturas_json,
            datos.get("score_prefiltrado", 0),
            datos.get("score_clip"),
            datos.get("score_deepface"),
            datos.get("score_final")
        ))
        conn.commit()
    except Exception as e:
        print(f"❌ Error al guardar en la base: {e}")

def guardar_log_csv(nombre_archivo, lista_dict):
    if not lista_dict:
        return
    df = pd.DataFrame(lista_dict)
    df.to_csv(nombre_archivo, index=False)

def elegir_db_y_tabla():
    db_folder = os.path.join(os.path.dirname(__file__), "..", "database")
    archivos_db = [f for f in listdir(db_folder) if isfile(join(db_folder, f)) and f.endswith(".db")]

    if not archivos_db:
        print("❌ No hay bases de datos disponibles.")
        return None, None

    print("Bases de datos disponibles:")
    for i, db in enumerate(archivos_db, 1):
        print(f"{i}. {db}")
    idx = int(input("Elegí el número de la base de datos: ")) - 1
    db_path = join(db_folder, archivos_db[idx])

    conn = sqlite3.connect(db_path)
    crear_tablas_si_no_existen(conn)  # <-- Asegura estructuras

    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tablas = [t[0] for t in cursor.fetchall()]
    print("Tablas disponibles:")
    for i, tabla in enumerate(tablas, 1):
        print(f"{i}. {tabla}")
    idx_tabla = int(input("Elegí el número de la tabla de comentarios: ")) - 1
    tabla_elegida = tablas[idx_tabla]

    return conn, tabla_elegida

def guardar_post_scrapeado(conn, post_url):
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS posts_scrapeados (
            url TEXT PRIMARY KEY
        )
    """)
    cursor.execute("INSERT OR IGNORE INTO posts_scrapeados (url) VALUES (?)", (post_url,))
    conn.commit()

def guardar_comentarios(conn, comentarios):
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS comentarios (
            username TEXT,
            comentario TEXT,
            fecha TEXT,
            post_url TEXT
        )
    """)
    for c in comentarios:
        cursor.execute("""
            INSERT INTO comentarios (username, comentario, fecha, post_url)
            VALUES (?, ?, ?, ?)
        """, (c["username"], c["comentario"], c["fecha"], c["post_url"]))
    conn.commit()

def guardar_comentarios_csv(comentarios, archivo):
    if not comentarios:
        return
    df = pd.DataFrame(comentarios)
    df.to_csv(archivo, index=False)

def usuario_ya_filtrado(conn, username):
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM usuarios_filtrados WHERE username = ?", (username,))
    return cursor.fetchone() is not None

def usuario_descartado(conn, username):
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM descartados WHERE username = ?", (username,))
    return cursor.fetchone() is not None

def agregar_comentario_a_filtrado(conn, username, comentario):
    cursor = conn.cursor()
    cursor.execute("SELECT comentarios FROM usuarios_filtrados WHERE username = ?", (username,))
    fila = cursor.fetchone()
    if fila:
        comentarios_actuales = fila[0] or ""
        comentarios_actuales += f"\n{comentario}"
        cursor.execute("UPDATE usuarios_filtrados SET comentarios = ? WHERE username = ?", (comentarios_actuales, username))
        conn.commit()
        
def cargar_posts_scrapeados(conn):
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS posts_scrapeados (
            url TEXT PRIMARY KEY
        )
    """)
    cursor.execute("SELECT url FROM posts_scrapeados")
    return set(row[0] for row in cursor.fetchall())

def extraer_usuarios_unicos(conn, tabla_origen="comentarios", tabla_destino="usuarios"):
    cursor = conn.cursor()

    # Crear tabla destino si no existe
    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {tabla_destino} (
            username TEXT PRIMARY KEY
        )
    """)

    # Extraer usernames únicos desde la tabla de comentarios
    cursor.execute(f"""
        INSERT OR IGNORE INTO {tabla_destino} (username)
        SELECT DISTINCT username FROM {tabla_origen}
    """)

    conn.commit()
    print(f"✅ Usuarios únicos extraídos desde '{tabla_origen}' a '{tabla_destino}'")

def descartar_usuario_por_perfil(conn, username, razones):
    """
    Marca un usuario como descartado dentro de la tabla usuarios_filtrados,
    almacenando el motivo.
    """
    cursor = conn.cursor()
    motivo = ", ".join(razones)
    cursor.execute("""
        UPDATE usuarios_filtrados 
        SET filtro_descartado = 1, motivo_descartado = ?
        WHERE username = ?
    """, (motivo, username))
    conn.commit()
    print(f"🚫 Usuario {username} descartado — Motivo(s): {motivo}")

def guardar_resultado_analisis_perfil(conn, username, datos, resultado):
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE usuarios_filtrados SET 
            publicaciones = ?, seguidores = ?, seguidos = ?, perfil_privado = ?, 
            bio = ?, historias_destacadas = ?, links_externos = ?, 
            score_prefiltrado = ?, score_clip = ?, score_deepface = ?, 
            score_final = ?, motivo_descartado = NULL
        WHERE username = ?
    """, (
        datos["publicaciones"],
        datos["seguidores"],
        datos["seguidos"],
        int(datos["perfil_privado"]),  # asegurate boolean en int
        datos["bio"],
        datos["historias_destacadas"],
        datos["links_externos"],
        resultado.get("score_prefiltrado", 0),
        resultado.get("score_clip"),
        resultado.get("score_deepface"),
        resultado.get("score_final"),
        username
    ))
    conn.commit()


def descartar_usuario_por_perfil(conn, username, razones):
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE usuarios_filtrados 
        SET motivo_descartado = ?, filtro_descartado = 1
        WHERE username = ?
    """, (", ".join(razones), username))
    conn.commit()