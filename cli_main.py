import argparse
import sqlite3
import os
import time
from lead_generator.scraping.extraer_comentarios import extraer_comentarios
from lead_generator.scraping.extraer_datos_perfil import extraer_datos_perfil
from lead_generator.filtro.filtro_comentarios import filtrar_comentarios_por_usuarios
from lead_generator.filtro.filtro_perfiles import filtrar_perfil_por_datos
from lead_generator.scoring.score_bio import scorear_bio
from lead_generator.scoring.score_global import scorear_fotos_por_carpeta, scorear_usuario_global
from lead_generator.utils import iniciar_driver, iniciar_driver_movil, obtener_driver_logueado, cerrar_driver
from lead_generator.auth.login import login_instagram, login_instagram_movil, pedir_credenciales
from config import DB_PATH, IMG_DIR
from lead_generator.utils.db import (
    crear_conexion,
    guardar_comentarios,
    guardar_post_scrapeado,
    usuario_ya_filtrado,
    usuario_descartado,
    agregar_comentario_a_filtrado,
    cargar_posts_scrapeados,
    iniciar_db,
    guardar_resultado_analisis_perfil, 
    descartar_usuario_por_perfil
)
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("filtrado_perfiles.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)

def etapa_extraer_comentarios(conn, driver):
    extraer_comentarios(conn, driver)

def etapa_filtrar_comentarios(conn):
    filtrar_comentarios_por_usuarios(conn, debug=True)

def etapa_filtrar_perfiles(conn, driver):
    cursor = conn.cursor()
    cursor.execute("SELECT username FROM usuarios_filtrados")
    usuarios = cursor.fetchall()
    time.sleep(10)
    usuarios_max = 10  # ejemplo para testear con solo 10
    for idx, (username,) in enumerate(usuarios):
        if idx >= usuarios_max:
            break
        try:
            print(f"Analizando perfil de {username}")
            datos = extraer_datos_perfil(username, driver)
            resultado = filtrar_perfil_por_datos(datos)

            logging.info(f"🧾 {username} | Bio: {datos['bio'][:40]}")
            logging.info(f"📊 Publicaciones: {datos['publicaciones']}, Seguidores: {datos['seguidores']}, Seguidos: {datos['seguidos']}, Historias: {datos['historias_destacadas']}")

            guardar_resultado_analisis_perfil(conn, username, datos, resultado)
            if resultado["score_prefiltrado"] < -1.0:
                descartar_usuario_por_perfil(conn, username, resultado["razones"])
                continue
            print(f"""
                📝 Usuario procesado: {username}
                📊 Score prefiltrado: {datos.get('score_prefiltrado', '')}
                🔍 Profesión: {datos.get('profesion_estimada', '')}
                🌍 Localizaciones: {datos.get('localizaciones', [])}
                🎭 Culturas: {datos.get('culturas', [])}
                💬 Bio: {datos.get('bio', '')}
                """)
        except Exception as e:
            logging.error(f"⚠️ Error al procesar {username}: {e}", exc_info=True)
    conn.commit()

def etapa_scorear_bios(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT username, bio FROM usuarios_filtrados")
    for username, bio in cursor.fetchall():
        result = scorear_bio(bio)
        for k, v in result.items():
            cursor.execute(f"UPDATE usuarios_filtrados SET {k} = ? WHERE username = ?", (v, username))
    conn.commit()

def etapa_scorear_fotos(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT username FROM usuarios")
    for (username,) in cursor.fetchall():
        carpeta = os.path.join(IMG_DIR, username)
        if os.path.exists(carpeta):
            score = scorear_fotos_por_carpeta(carpeta)
            cursor.execute("UPDATE usuarios SET score_fotos = ? WHERE username = ?", (score, username))
    conn.commit()

def etapa_scorear_global(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT username, score_bio, score_fotos, score_username, score_comentario FROM usuarios")
    for row in cursor.fetchall():
        username = row[0]
        user_data = {
            "score_bio": row[1],
            "score_fotos": row[2],
            "score_username": row[3],
            "score_comentario": row[4],
        }
        global_score = scorear_usuario_global(user_data)
        cursor.execute("UPDATE usuarios SET score = ? WHERE username = ?", (global_score, username))
    conn.commit()

def ejecutar_pipeline_completo(conn, driver):
    etapa_extraer_comentarios(conn, driver)
    etapa_filtrar_comentarios(conn)
    etapa_filtrar_perfiles(conn, driver)
    etapa_scorear_bios(conn)
    etapa_scorear_fotos(conn)
    etapa_scorear_global(conn)

def main():
    parser = argparse.ArgumentParser(description="Lead Generator CLI")
    parser.add_argument("etapa", choices=[
        "extraer_comentarios",
        "filtrar_comentarios",
        "filtrar_perfiles",
        "scorear_bios",
        "scorear_fotos",
        "scorear_global",
        "pipeline"
    ])
    parser.add_argument("--usuario", help="Instagram username")
    parser.add_argument("--password", help="Instagram password")
    args = parser.parse_args()

    conn = crear_conexion()
    driver = None

    necesita_driver = args.etapa in ["extraer_comentarios", "filtrar_perfiles", "scorear_fotos", "pipeline"]

    if necesita_driver:
        if args.etapa == "scorear_fotos":
            driver = iniciar_driver_movil(headless=False)
        else:
            driver = iniciar_driver(headless=False)

        if not args.usuario or not args.password:
            args.usuario, args.password = pedir_credenciales()

        # Login
        if args.etapa == "scorear_fotos":
            login_instagram_movil(driver, args.usuario, args.password)
        else:
            login_instagram(driver, args.usuario, args.password)

    try:
        if args.etapa == "extraer_comentarios":
            etapa_extraer_comentarios(conn, driver)
        elif args.etapa == "filtrar_comentarios":
            etapa_filtrar_comentarios(conn)
        elif args.etapa == "filtrar_perfiles":
            etapa_filtrar_perfiles(conn, driver)
        elif args.etapa == "scorear_bios":
            etapa_scorear_bios(conn)
        elif args.etapa == "scorear_fotos":
            etapa_scorear_fotos(conn)
        elif args.etapa == "scorear_global":
            etapa_scorear_global(conn)
        elif args.etapa == "pipeline":
            ejecutar_pipeline_completo(conn, driver)
    finally:
        conn.close()
        if driver:
            driver.quit()

if __name__ == "__main__":
    main()