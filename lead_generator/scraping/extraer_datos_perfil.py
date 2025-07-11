from selenium.webdriver.common.by import By
import re
from lead_generator.utils import parse_num, convertir_a_numero, parsear_km, detectar_geolocalizacion_en_bio
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
import time
from lead_generator.utils import parsear_km, extraer_link_real


def contar_historias_destacadas(driver):
    """
    Retorna la cantidad de historias destacadas en el perfil abierto actualmente.
    Basado en la cantidad de elementos <canvas> visibles, menos la foto de perfil.
    """
    try:
        WebDriverWait(driver, 3).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, "canvas"))
        )

        canvas_elements = driver.find_elements(By.TAG_NAME, "canvas")
        visibles = [c for c in canvas_elements if c.is_displayed()]
        total_canvas = len(visibles)

        historias = max(0, total_canvas - 1)
        print(f"🟡 Historias destacadas detectadas: {historias}")
        return historias
    except Exception as e:
        print(f"❌ Error detectando historias destacadas: {e}")
        return 0

def extraer_datos_perfil(username, driver):
    url = f"https://www.instagram.com/{username}/"
    driver.get(url)
    time.sleep(3)  # simple espera inicial

    datos = {
        "username": username,
        "comentarios": "",
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
        "score_mujer": 0.0,
        "motivo_penalizado_mujer": "",
        "score_bio": 0.0,
        "score_clip": None,
        "score_deepface": None,
        "score_final": None
    }

    # Publicaciones, seguidores, seguidos
    try:
        elementos = driver.find_elements(By.XPATH, '//header//li')
        for el in elementos:
            txt = el.text.lower()
            if "publicacion" in txt:
                datos["publicaciones"] = int(txt.split()[0].replace('.', '').replace(',', ''))
            elif "seguidor" in txt:
                datos["seguidores"] = parsear_km(txt.split()[0])
            elif "seguido" in txt:
                datos["seguidos"] = parsear_km(txt.split()[0])
        print(f"📊 Stats — Pub: {datos['publicaciones']}, Seg: {datos['seguidores']}, Sig: {datos['seguidos']}")
    except Exception as e:
        print(f"[WARN] Error leyendo stats para {username}: {e}")

    # Bio: intenta primero con aria-disabled
    try:
        bio_element = driver.find_element(By.XPATH, "//header//div[@aria-disabled='false']//span")
        datos["bio"] = bio_element.text.strip()
        print(f"📋 Bio (aria-disabled) para {username}: '{datos['bio']}'")
    except NoSuchElementException:
        # Fallback: encuentra el primer span con texto válido que no contenga stats
        try:
            bio_elements = driver.find_elements(By.XPATH, "//header//span[@dir='auto']")
            textos_validos = []
            for el in bio_elements:
                txt = el.text.strip()
                txt_lower = txt.lower()
                if any(stat in txt_lower for stat in ["seguidores", "seguidos", "publicaciones"]):
                    continue
                if txt:  # no filtres por longitud
                    textos_validos.append(txt)

            if textos_validos:
                datos["bio"] = textos_validos[0]
                print(f"📋 Bio (fallback primer válido) para {username}: '{datos['bio']}'")
            else:
                datos["bio"] = ""
                print(f"[WARN] Fallback sin resultados válidos para bio en {username}")
        except Exception as e:
            datos["bio"] = ""
            print(f"[ERROR] Buscando bio fallback para {username}: {e}")


    # Links externos
    links = driver.find_elements(By.XPATH, '//a[contains(@href, "l.instagram.com")]')
    for link in links:
        text = link.text.strip()
        if link.is_displayed() and text:
            href = link.get_attribute("href")
            datos["links_externos"] = extraer_link_real(href)
            break

    # Historias destacadas
    try:
        canvases = driver.find_elements(By.TAG_NAME, "canvas")
        datos["historias_destacadas"] = max(len(canvases) - 1, 0)
    except:
        datos["historias_destacadas"] = 0

    # Perfil privado
    try:
        privado = driver.find_elements(By.XPATH, '//*[contains(text(),"Esta cuenta es privada")]')
        datos["perfil_privado"] = len(privado) > 0
    except:
        datos["perfil_privado"] = False

    return datos




