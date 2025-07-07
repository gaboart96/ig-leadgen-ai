# === extraer_comentarios.py (refactorizado) ===
import time, random, re
from inputimeout import inputimeout, TimeoutOccurred
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

from lead_generator.utils import (
    normalizar_texto, es_fecha,
    guardar_post_scrapeado, cargar_posts_scrapeados,
    guardar_comentarios, guardar_comentarios_csv
)
from config import GUARDAR_EN_DB, GUARDAR_EN_CSV

def obtener_posts_de_perfil(driver, username, max_posts=20):
    driver.get(f"https://www.instagram.com/{username}/")
    time.sleep(5)
    post_links, vistos = [], set()
    while len(post_links) < max_posts:
        enlaces = driver.find_elements(By.XPATH, '//a[contains(@href, "/p/")]')
        for a in enlaces:
            href = a.get_attribute("href")
            if href and href not in vistos:
                post_links.append(href)
                vistos.add(href)
                if len(post_links) >= max_posts:
                    break
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
    return post_links

def expandir_comentarios(driver):
    wait = WebDriverWait(driver, 3)
    actions = ActionChains(driver)
    scroll_prev, no_avance = -1, 0
    ocultos_vistos, iteraciones = False, 0

    for _ in range(300):
        if ocultos_vistos:
            iteraciones += 1
            if iteraciones >= 10:
                break

        hizo_algo = False
        try:
            actions.move_to_element_with_offset(driver.find_element(By.TAG_NAME, "body"), 0, 0).perform()
        except: pass

        for xpath, label in [
            ('svg[aria-label="Cargar más comentarios"]', "Cargar más comentarios"),
            ('//span[contains(text(), "Ver comentarios ocultos")]/ancestor::div[@role="button"]', "Ver comentarios ocultos")
        ]:
            try:
                boton = driver.find_element(By.CSS_SELECTOR, xpath) if 'svg' in xpath else driver.find_element(By.XPATH, xpath)
                driver.execute_script("arguments[0].scrollIntoView(true);", boton)
                boton.click()
                time.sleep(random.uniform(1, 1.5))
                hizo_algo = True
                if 'ocultos' in label:
                    ocultos_vistos = True
                break
            except: pass

        try:
            for boton in driver.find_elements(By.XPATH, '//button[.//*[contains(text(), "Ver respuestas")]]'):
                try:
                    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", boton)
                    time.sleep(random.uniform(0.3, 0.6))
                    boton.click()
                    hizo_algo = True
                except: continue
        except: pass

        if not hizo_algo:
            try:
                scroll = driver.find_element(By.XPATH, '(//div[div/div/div/div/a])[1]')
                driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scroll)
                wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, 'svg[aria-label="Cargando..."]')))
                time.sleep(random.uniform(1, 1.5))
                nuevo_scroll = driver.execute_script("return arguments[0].scrollTop", scroll)
                no_avance = no_avance + 1 if nuevo_scroll == scroll_prev else 0
                scroll_prev = nuevo_scroll
                if no_avance >= 5:
                    break
            except: break
        elif not hizo_algo:
            break
    return True

def extraer_comentarios_de_post(driver, post_url, usuario_actual, max_comentarios=5000):
    driver.get(post_url)
    time.sleep(5)
    expandir_comentarios(driver)
    time.sleep(2)

    comentarios, vistos = [], set()
    for bloque in driver.find_elements(By.XPATH, '//div'):
        try:
            clases = bloque.get_attribute("class").split()
            if not clases or not any(c.startswith("_a") or re.fullmatch(r"x\w{6,7}", c) for c in clases):
                continue

            username_elem = bloque.find_element(By.XPATH, './/a[starts-with(@href, "/")]')
            username = username_elem.text.strip()
            if not username or username.lower() in {usuario_actual.lower()} or es_fecha(username):
                continue

            comentario_el = next((span for span in bloque.find_elements(By.XPATH, './/span')
                                  if span.text.strip() and len(span.text.strip()) > 1), None)
            if not comentario_el:
                continue

            comentario = comentario_el.text.strip()
            if es_fecha(comentario):
                continue

            clave = (username.lower(), normalizar_texto(comentario))
            if clave in vistos:
                continue
            vistos.add(clave)

            try:
                fecha = bloque.find_element(By.XPATH, './/time').get_attribute("datetime")
            except:
                fecha = ""

            comentarios.append({
                "username": username,
                "comentario": comentario,
                "fecha": fecha,
                "post_url": post_url
            })

            print(f"[{len(comentarios)}] ✅ @{username}: {comentario} ({fecha})")
            if len(comentarios) >= max_comentarios:
                break

        except: continue

    print(f"\n🟢 Total comentarios extraídos: {len(comentarios)}")
    return comentarios, len(comentarios) > 0

# === NUEVA FUNCION EXPORTADA ===
def extraer_comentarios(conn, driver):
    modo = input("\n1️⃣  Perfil completo\n2️⃣  Post individual\nElegí 1 o 2: ").strip()
    while modo not in {"1", "2"}:
        modo = input("Por favor, ingresá 1 o 2: ").strip()

    posts_scrapeados = cargar_posts_scrapeados(conn)
    comentarios_total = []

    if modo == "1":
        username = input("Username de IG (sin @): ").strip()
        CSV_FILENAME = f"comentarios_{username}.csv"
        post_urls = obtener_posts_de_perfil(driver, username)
    else:
        url = input("Pegá la URL del post (/p/): ").strip()
        if "/p/" not in url:
            print("⚠️ Link inválido.")
            return
        post_urls = [url]
        slug = url.strip('/').split("/")[-1]
        CSV_FILENAME = f"comentarios_{slug}.csv"
        username = "manual"

    for post_url in post_urls:
        if post_url in posts_scrapeados:
            try:
                eleccion = inputimeout(prompt=f"Post ya scrapeado: {post_url}\n>> Ingresá 's' para scrapear o cualquier otra tecla para saltar (10s): ", timeout=10)
                if eleccion.strip().lower() != "s":
                    continue
            except TimeoutOccurred:
                continue

        comentarios, exito = extraer_comentarios_de_post(driver, post_url, username)
        if exito:
            comentarios_total.extend(comentarios)
            if GUARDAR_EN_DB:
                guardar_post_scrapeado(conn, post_url)
                guardar_comentarios(conn, comentarios)
            if GUARDAR_EN_CSV:
                guardar_comentarios_csv(comentarios, CSV_FILENAME)

    print(f"\n✅ {len(comentarios_total)} comentarios procesados en total.")
