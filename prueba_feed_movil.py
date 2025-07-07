from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pathlib import Path
import time
from PIL import Image
import io
import requests
from getpass import getpass

def iniciar_driver_movil():

    chrome_options = Options()

    mobile_emulation = {
        "deviceMetrics": { "width": 1920, "height": 1080, "pixelRatio": 3.0 },  # iPhone X real
        "userAgent": (
            "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) "
            "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 "
            "Mobile/15E148 Safari/604.1"
        )
    }

    chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
    driver = webdriver.Chrome(options=chrome_options)
    return driver

def login_instagram(driver, username, password, guardar_info=False):
    driver.get("https://www.instagram.com/accounts/login/")
    
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "username")))
    driver.find_element(By.NAME, "username").send_keys(username)
    driver.find_element(By.NAME, "password").send_keys(password)

    login_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//div[@role="button" and @aria-label="Iniciar sesión"]'))
    )
    login_btn.click()

    # Omitir "Guardar información" o no
    try:
        if guardar_info:
            guardar_btn = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((
                    By.XPATH,
                    '//span[contains(text(), "Guardar información")]/ancestor::div[@role="button"]'
                ))
            )
            guardar_btn.click()
        else:
            ahora_no_btn = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((
                    By.XPATH,
                    '//span[contains(text(), "Ahora no")]/ancestor::div[@role="button"]'
                ))
            )
            ahora_no_btn.click()
    except Exception as e:
        print("⚠️ No apareció la opción de guardar información o fue omitida automáticamente:", e)

    print("✅ Login completado.")

def detectar_y_guardar_canvas(driver, username, carpeta_destino):
    perfil_url = f"https://www.instagram.com/{username}/"
    driver.get(perfil_url)

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//h2 | //h1'))
    )

    time.sleep(2)  # Espera extra para asegurar carga de stories destacadas

    canvas_elements = driver.find_elements(By.TAG_NAME, "canvas")

    print(f"🖼️ Total de <canvas> detectados: {len(canvas_elements)}")

    historias_destacadas = max(0, len(canvas_elements) - 1)
    print(f"✨ Cantidad de historias destacadas detectadas: {historias_destacadas}")

    Path(carpeta_destino).mkdir(parents=True, exist_ok=True)

    for i, canvas in enumerate(canvas_elements):
        png = canvas.screenshot_as_png
        with open(f"{carpeta_destino}/canvas_{i+1}.png", "wb") as f:
            f.write(png)
        print(f"✅ Canvas {i+1} guardado.")

    print("🔍 Esperando inspección manual...")
    input("Presioná Enter para cerrar el navegador...")

# -------------------------
# EJECUCIÓN
# -------------------------
if __name__ == "__main__":
    USUARIO = input("Usuario de Instagram: ")
    PASSWORD = getpass("Contraseña: ")
    PERFIL_URL = input("URL del perfil a analizar: ").strip()
    GUARDAR_INFO = input("¿Guardar sesión? (s/n): ").strip().lower() == "s"

    username = PERFIL_URL.strip("/").split("/")[-1]
    carpeta = f"output_canvas/{username}"

    driver = iniciar_driver_movil()

    try:
        login_instagram(driver, USUARIO, PASSWORD, guardar_info=GUARDAR_INFO)
        detectar_y_guardar_canvas(driver, username, carpeta)
    finally:
        driver.quit()
