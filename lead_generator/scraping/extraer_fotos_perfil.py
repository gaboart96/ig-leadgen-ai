from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pathlib import Path
from PIL import Image
import io
import requests
import time
from lead_generator.utils import iniciar_driver

# === CONFIGURACIÓN PREVIA ===
IMAGENES_POR_FILA = 3
FILAS_POR_SCROLL = 2
IMAGENES_POR_SCROLL = IMAGENES_POR_FILA * FILAS_POR_SCROLL

def capturar_foto_perfil(driver, username, ruta_salida):
    perfil_url = f"https://www.instagram.com/{username}/"
    driver.get(perfil_url)
    try:
        img = WebDriverWait(driver, 2).until(
            EC.presence_of_element_located(
                (By.XPATH, '//img[contains(@alt, "Foto del perfil")]')
            )
        )
        src = img.get_attribute("src")
        img_data = requests.get(src).content
        with open(ruta_salida, 'wb') as f:
            f.write(img_data)
        print(f"✅ Foto de perfil guardada en: {ruta_salida}")
        return True
    except Exception as e:
        print(f"❌ Error al capturar foto de perfil: {e}")
        return False

def obtener_margen_bottom(driver, elemento):
    return driver.execute_script("""
        const style = window.getComputedStyle(arguments[0]);
        return parseFloat(style.marginBottom);
    """, elemento)

def extraer_feed_fotos(driver, username, carpeta_destino, max_posts=12):
    perfil_url = f"https://www.instagram.com/{username}/"
    driver.get(perfil_url)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//h2 | //h1'))
    )

    ruta_foto_perfil = f"{carpeta_destino}/foto_perfil.jpg"
    Path(carpeta_destino).mkdir(parents=True, exist_ok=True)
    capturar_foto_perfil(driver, username, ruta_foto_perfil)

    try:
        # Asegura que está en el perfil
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//h1 | //h2'))
        )

        # Espera el feed, con más tiempo y con un XPATH más flexible
        feed_div = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((
                By.XPATH,
                '//div[contains(@style, "flex-direction: column")]//img'
            ))
        )
        y = feed_div.location['y']
        driver.execute_script(f"window.scrollTo({{top: {y}, behavior: 'instant'}});")
        print("✅ Navegó correctamente al feed.")
    except Exception as e:
        print("❌ No se pudo encontrar el feed:", e)
        return

    a_tags = []
    hrefs_vistos = set()
    fila_index = 0
    filas = driver.find_elements(By.XPATH, '//div[contains(@style, "flex-direction: column")]/div')

    while len(a_tags) < max_posts:
        if fila_index >= len(filas):
            break
        fila = filas[fila_index]
        fila_index += 1
        celdas = fila.find_elements(By.XPATH, "./div")
        for celda in celdas:
            try:
                a = celda.find_element(By.XPATH, ".//a")
                href = a.get_attribute("href")
                if href and href not in hrefs_vistos:
                    hrefs_vistos.add(href)
                    a_tags.append(a)
                    if len(a_tags) >= max_posts:
                        break
            except:
                continue

    png = driver.get_screenshot_as_png()
    screenshot = Image.open(io.BytesIO(png))

    altura_fila = filas[0].size['height']
    margen_vertical = obtener_margen_bottom(driver, filas[0]) or 0
    ancho_imagen = a_tags[0].size['width']
    y_inicial = filas[0].location_once_scrolled_into_view['y']
    x_posiciones = [int(a_tags[i].location_once_scrolled_into_view['x']) for i in range(IMAGENES_POR_FILA)]

    scroll_offset = 0

    for i in range(0, len(a_tags), IMAGENES_POR_SCROLL):
        screenshot = Image.open(io.BytesIO(driver.get_screenshot_as_png()))
        screenshot.save(f"{carpeta_destino}/feed_{i//IMAGENES_POR_SCROLL}.png")
        for j in range(IMAGENES_POR_SCROLL):
            idx = i + j
            if idx >= len(a_tags):
                break
            fila_num = idx // IMAGENES_POR_FILA
            col_num = idx % IMAGENES_POR_FILA
            x = x_posiciones[col_num]
            y_absoluto = int(y_inicial + fila_num * (altura_fila + margen_vertical))
            y = y_absoluto - scroll_offset
            w = int(ancho_imagen)
            h = int(altura_fila)
            crop = screenshot.crop((x, y, x + w, y + h))
            crop.save(f"{carpeta_destino}/post_{idx+1}.png")
            print(f"✅ Recorte guardado: post_{idx+1}.png")

        if i + IMAGENES_POR_SCROLL < len(a_tags):
            desplazamiento = FILAS_POR_SCROLL * (altura_fila + margen_vertical)
            driver.execute_script(f"window.scrollBy(0, {desplazamiento});")
            scroll_offset += desplazamiento
            time.sleep(0.6)

