# lead_generator/core/driver_session.py
from lead_generator.auth.login import pedir_credenciales, login_instagram
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def iniciar_driver(headless=True):
    options = Options()
    if headless:
        options.add_argument("--headless=new")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    return webdriver.Chrome(options=options)

def iniciar_driver_movil(headless=True):
    mobile_emulation = {"deviceName": "iPhone X"}
    options = Options()
    options.add_experimental_option("mobileEmulation", mobile_emulation)
    if headless:
        options.add_argument("--headless=new")
    options.add_argument("--window-size=1920,1080")
    return webdriver.Chrome(options=options)


_driver_global = None

def obtener_driver_logueado(movil=False, headless=True):
    """
    Inicia sesión en Instagram y guarda el driver en cache para reuso.
    """
    global _driver_global

    if _driver_global is None:
        print("[INFO] Iniciando driver único...")
        try:
            _driver_global = iniciar_driver_movil(headless) if movil else iniciar_driver(headless)
            usuario, password = pedir_credenciales()
            login_instagram(_driver_global, usuario, password)
            print("[INFO] Sesión iniciada correctamente.")
        except Exception as e:
            print(f"[ERROR] Falló la sesión: {e}")
            if _driver_global:
                print("[DEBUG] Dejando navegador abierto para inspección.")
                input("Presioná Enter para cerrar manualmente...")
            else:
                print("[ERROR] No se pudo iniciar el driver.")
            raise

    return _driver_global

def cerrar_driver():
    global _driver_global
    if _driver_global:
        print("[INFO] Cerrando driver único...")
        _driver_global.quit()
        _driver_global = None
