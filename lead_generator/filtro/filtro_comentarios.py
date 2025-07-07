import sqlite3
import os
import re
import unicodedata
from os import listdir
from os.path import isfile, join
from lead_generator.utils import normalizar_texto, elegir_db_y_tabla, es_spam, extraer_usuarios_unicos, penalizacion_femenina


# -# === filtro_comentarios.py ===
from lead_generator.utils.db import (
    usuario_ya_filtrado,
    usuario_descartado,
    agregar_comentario_a_filtrado,
    descartar_usuario_por_perfil,
    guardar_usuario_filtrado
)


def filtrar_comentario_con_motivo(username, comentario):
    if len(username) < 3:
        return False, "Username muy corto"
    if len(comentario) < 4:
        return False, "Comentario muy corto"
    if es_spam(username, comentario, debug=True):
        return False, "Detectado como spam"
    return True, ""

def filtrar_comentarios_por_usuarios(conn, debug=False):
    cursor = conn.cursor()
    cursor.execute("SELECT username, comentario FROM comentarios")
    filas = cursor.fetchall()

    lista_comentarios = [{"username": u.strip().lower(), "comentario": c.strip()} for u, c in filas]

    nuevos_usuarios = []
    ya_existentes = 0
    descartados = 0

    for comentario in lista_comentarios:
        username = comentario["username"]
        texto = comentario["comentario"]

        if usuario_descartado(conn, username):
            if debug:
                print(f"⏩ Usuario {username} ya descartado anteriormente")
            descartados += 1
            continue

        if usuario_ya_filtrado(conn, username):
            agregar_comentario_a_filtrado(conn, username, texto)
            ya_existentes += 1
            continue

        # Penalizaciones acumulativas
        penalizacion_total = 0.0
        penalizacion_total += es_spam(username, texto, debug=debug)
        penalizacion_total += penalizacion_femenina(username, "", texto)

        if debug:
            print(f"🧮 Score prefiltrado total: {penalizacion_total}")

        if penalizacion_total < -1.0:
            descartar_usuario_por_perfil(conn, username, ["score prefiltrado muy bajo"])
            descartados += 1
            continue

        datos_usuario = {
            "username": username,
            "comentarios": texto,
            "fotos_analizadas": 0,
            "fotos_sin_personas": 0,
            "flag_incompleto": True,
            "filtro_descartado": False,
            "motivo_descartado": "",
            "bio": "",
            "perfil_privado": False,
            "publicaciones": 0,
            "seguidores": 0,
            "seguidos": 0,
            "historias_destacadas": 0,
            "links_externos": 0,
            "edad_estimada": None,
            "profesion_estimada": None,
            "localizaciones": [],
            "culturas": [],
            "score_prefiltrado": penalizacion_total,
            "score_clip": None,
            "score_deepface": None,
            "score_final": None
        }

        guardar_usuario_filtrado(conn, datos_usuario)
        nuevos_usuarios.append(username)

        print(f"✅ Usuario {username} agregado con score_prefiltrado: {penalizacion_total}")

    print(f"\n🧹 Resultado del filtrado:")
    print(f"✅ Nuevos usuarios filtrados: {len(nuevos_usuarios)}")
    print(f"🔁 Comentarios añadidos a usuarios ya existentes: {ya_existentes}")
    print(f"🚫 Usuarios descartados: {descartados}")

    return nuevos_usuarios



# ---------------------------
# EJECUCIÓN INDEPENDIENTE
# ---------------------------



if __name__ == "__main__":
    conn, tabla = elegir_db_y_tabla()
    if conn and tabla:
        extraer_usuarios_unicos(conn, tabla)
        conn.close()
