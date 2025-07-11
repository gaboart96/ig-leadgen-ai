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
            bio TEXT,
            perfil_privado BOOLEAN,
            publicaciones INTEGER,
            seguidores INTEGER,
            seguidos INTEGER,
            historias_destacadas INTEGER,
            links_externos TEXT,
            edad_estimada REAL,
            profesion TEXT,
            localizaciones TEXT,
            culturas TEXT,
            score_malo REAL,
            motivo_penalizado_malo TEXT,
            score_mujer REAL,
            motivo_penalizado_mujer TEXT,
            score_bio REAL,          
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
        CREATE TABLE IF NOT EXISTS posts_scrapeados (
            url TEXT PRIMARY KEY
        )
    """)

    cursor.execute(""" CREATE TABLE IF NOT EXISTS descartados_malos AS
    SELECT * FROM usuarios_filtrados WHERE 0
    """)

    cursor.execute(""" CREATE TABLE IF NOT EXISTS descartados_mujer AS
    SELECT * FROM usuarios_filtrados WHERE 0
    """)
   

    conn.commit()
def guardar_usuario_filtrado(conn, datos):
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO usuarios_filtrados (
            username, comentarios, bio, perfil_privado, publicaciones, seguidores, seguidos,
            historias_destacadas, links_externos, edad_estimada, profesion,
            localizaciones, culturas,
            score_malo, motivo_penalizado_malo,
            score_mujer, motivo_penalizado_mujer,
            score_bio, score_clip, score_deepface, score_final
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        datos["username"],
        datos.get("comentarios", ""),
        datos.get("bio", ""),
        int(datos.get("perfil_privado", False)),
        datos.get("publicaciones", 0),
        datos.get("seguidores", 0),
        datos.get("seguidos", 0),
        datos.get("historias_destacadas", 0),
        datos.get("links_externos", ""),
        datos.get("edad_estimada"),
        datos.get("profesion"),
        json.dumps(datos.get("localizaciones", [])),
        json.dumps(datos.get("culturas", [])),
        datos.get("score_malo", 0.0),
        datos.get("motivo_penalizado_malo"),
        datos.get("score_mujer", 0.0),
        datos.get("motivo_penalizado_mujer"),
        datos.get("score_bio"),
        datos.get("score_clip"),
        datos.get("score_deepface"),
        datos.get("score_final")
    ))
    conn.commit()
    
def guardar_resultado_analisis_perfil(conn, datos):
    cursor = conn.cursor()
    username = datos["username"]  # <-- aquí lo extraes del dict

    cursor.execute("""
        UPDATE usuarios_filtrados SET 
            publicaciones = ?, seguidores = ?, seguidos = ?, perfil_privado = ?, 
            bio = ?, historias_destacadas = ?, links_externos = ?, 
            edad_estimada = ?, profesion = ?, localizaciones = ?, culturas = ?, 
            score_malo = ?, motivo_penalizado_malo = ?,
            score_mujer = ?, motivo_penalizado_mujer = ?,
            score_bio = ?, score_clip = ?, score_deepface = ?, score_final = ?
        WHERE username = ?
    """, (
        datos["publicaciones"],
        datos["seguidores"],
        datos["seguidos"],
        int(datos["perfil_privado"]),
        datos["bio"],
        datos["historias_destacadas"],
        datos["links_externos"],
        datos.get("edad_estimada"),
        datos.get("profesion"),
        ",".join(datos.get("localizaciones", [])),
        ",".join(datos.get("culturas", [])),
        datos["score_malo"],
        datos["motivo_penalizado_malo"],
        datos["score_mujer"],
        datos["motivo_penalizado_mujer"],
        datos.get("score_bio"),
        datos.get("score_clip"),
        datos.get("score_deepface"),
        datos.get("score_final"),
        username   # <-- el username para el WHERE va al final
    ))
    conn.commit()

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

    tablas = ["descartados_malos", "descartados_mujer"]
    for tabla in tablas:
        cursor.execute(f"SELECT 1 FROM {tabla} WHERE username = ?", (username,))
        if cursor.fetchone():
            return True  # Está en alguna tabla

    return False  # No está en ninguna

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

def descartar_usuario(conn, username, razones, tabla_destino):
    """
    Copia el usuario desde usuarios_filtrados a tabla_destino,
    poniendo el motivo en el campo correcto, y luego lo elimina de usuarios_filtrados.
    tabla_destino debe ser 'descartados_malos' o 'descartados_mujer'.
    """
    cursor = conn.cursor()
    motivo = ", ".join(razones)

    # Trae el registro original
    cursor.execute("SELECT * FROM usuarios_filtrados WHERE username = ?", (username,))
    row = cursor.fetchone()

    if not row:
        print(f"❌ No se encontró el usuario {username} en usuarios_filtrados.")
        return

    # Crea un diccionario del registro actual
    columns = [desc[0] for desc in cursor.description]
    data = dict(zip(columns, row))

    # Actualiza el motivo SOLO en el campo correspondiente
    if tabla_destino == "descartados_malos":
        data["motivo_penalizado_malo"] = motivo
    elif tabla_destino == "descartados_mujer":
        data["motivo_penalizado_mujer"] = motivo

    # Genera placeholders e inserta en la tabla destino
    placeholders = ", ".join("?" * len(data))
    column_names = ", ".join(data.keys())
    cursor.execute(
        f"INSERT INTO {tabla_destino} ({column_names}) VALUES ({placeholders})",
        tuple(data.values())
    )

    # Borra del origen
    cursor.execute("DELETE FROM usuarios_filtrados WHERE username = ?", (username,))
    conn.commit()

    print(f"🚫 Usuario {username} movido a {tabla_destino} — Motivo(s): {motivo}")

def guardar_resultado_analisis_perfil(conn, username, datos, resultado):
    cursor = conn.cursor()
    localizaciones_json = json.dumps(resultado["localizaciones"])
    culturas_json = json.dumps(resultado["culturas"])
    profesion_json = json.dumps(resultado["profesion"]) if isinstance(resultado["profesion"], dict) else json.dumps([resultado["profesion"]])
    cursor.execute("""
        UPDATE usuarios_filtrados SET 
            publicaciones = ?, 
            seguidores = ?, 
            seguidos = ?, 
            perfil_privado = ?, 
            bio = ?, 
            historias_destacadas = ?, 
            links_externos = ?,
            profesion = ?, 
            localizaciones = ?, 
            culturas = ?,
            score_malo = ?, 
            motivo_penalizado_malo = ?,
            score_mujer = ?, 
            motivo_penalizado_mujer = ?,
            score_bio = ?, 
            score_clip = ?, 
            score_deepface = ?, 
            score_final = ?
        WHERE username = ?
    """, (
        datos.get("publicaciones", 0),
        datos.get("seguidores", 0),
        datos.get("seguidos", 0),
        int(datos.get("perfil_privado", False)),
        datos.get("bio", ""),
        datos.get("historias_destacadas", 0),
        datos.get("links_externos", ""),
        profesion_json,
        localizaciones_json,
        culturas_json,
        resultado.get("score_malo", 0.0),
        resultado.get("motivo_penalizado_malo", ""),
        resultado.get("score_mujer", 0.0),
        resultado.get("motivo_penalizado_mujer", ""),
        resultado.get("score_bio", 0.0),
        resultado.get("score_clip"),
        resultado.get("score_deepface"),
        resultado.get("score_final"),
        username
    ))
    conn.commit()


