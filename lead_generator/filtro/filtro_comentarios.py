import sqlite3
import os
import re
import unicodedata
from os import listdir
from os.path import isfile, join

from lead_generator.utils import (
    normalizar_texto,
    elegir_db_y_tabla,
    es_spam,
    penalizacion_por_nombre_mujer,
    penalizacion_por_comentario_mujer
)

from lead_generator.utils.db import (
    usuario_ya_filtrado,
    usuario_descartado,
    agregar_comentario_a_filtrado,
    descartar_usuario,
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

    nuevos_usuarios = []
    ya_existentes = 0
    descartados = 0
    UMBRAL_SCORE = -1

    for fila in filas:
        username = fila[0].strip().lower()
        texto = fila[1].strip()

        if usuario_descartado(conn, username):
            if debug:
                print(f"⏩ Usuario {username} ya descartado anteriormente")
            descartados += 1
            continue

        if usuario_ya_filtrado(conn, username):
            #agregar_comentario_a_filtrado(conn, username, texto)
            ya_existentes += 1
            continue

        penal_nom_mujer, razones_nom_mujer = penalizacion_por_nombre_mujer(username)
        penal_com_mujer, razones_com_mujer = penalizacion_por_comentario_mujer(texto)

        penal_nom_malo, razones_nom_malo = es_spam(username)
        penal_com_malo, razones_com_malo = es_spam(texto)

        score_mujer = penal_nom_mujer + penal_com_mujer
        score_malo = penal_nom_malo + penal_com_malo

        razones_mujer = razones_nom_mujer + razones_com_mujer
        razones_malo = razones_nom_malo + razones_com_malo

        if score_mujer < UMBRAL_SCORE:
            descartar_usuario(conn, username, razones_mujer, "descartados_mujer")
            descartados += 1
            if debug:
                print(f"🚫 Usuario {username} descartado por mujer: {razones_mujer}")
            continue

        if score_malo < UMBRAL_SCORE:
            descartar_usuario(conn, username,  razones_malo, "descartados_malo")
            descartados += 1
            if debug:
                print(f"🚫 Usuario {username} descartado por mujer: {razones_malo}")
            continue

        datos_usuario = {
            "username": username,
            "comentarios": texto,
            "bio": "",
            "perfil_privado": False,
            "publicaciones": 0,
            "seguidores": 0,
            "seguidos": 0,
            "historias_destacadas": 0,
            "links_externos": "",
            "edad_estimada": None,
            "profesion": None,
            "localizaciones": [],
            "culturas": [],
            "score_malo": 0.0,
            "motivo_penalizado_malo": "",
            "score_mujer": round(score_mujer, 2),
            "motivo_penalizado_mujer": ", ".join(razones_mujer),
            "score_bio": None,
            "score_clip": None,
            "score_deepface": None,
            "score_final": None,
        }

        guardar_usuario_filtrado(conn, datos_usuario)
        nuevos_usuarios.append(username)

        if debug:
            print(f"✅ Usuario {username} agregado con score_mujer: {round(score_mujer, 2)} - Razones: {razones_mujer}")

    print(f"\n🧹 Resultado:")
    print(f"✅ Nuevos usuarios: {len(nuevos_usuarios)}")
    print(f"🔁 Comentarios añadidos a existentes: {ya_existentes}")
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