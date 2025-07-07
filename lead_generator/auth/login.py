# login.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import getpass
#from lead_generator.utils.driver import iniciar_driver
from selenium.webdriver.chrome.webdriver import WebDriver

def pedir_credenciales():
    IG_USER = input("Usuario de Instagram: ").strip()
    IG_PASS = getpass.getpass("Contraseña de Instagram: ").strip()
    return IG_USER, IG_PASS


def login_instagram(driver, username, password, guardar_info=False):
    print("🔄 Intentando login estilo escritorio...")
    driver.get("https://www.instagram.com/accounts/login/")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "username")))

    driver.find_element(By.NAME, "username").clear()
    driver.find_element(By.NAME, "username").send_keys(username)
    driver.find_element(By.NAME, "password").clear()
    driver.find_element(By.NAME, "password").send_keys(password)

    try:
        # Botón estilo escritorio (más tradicional)
        login_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//button[@type="submit"]'))
        )
        login_btn.click()
    except:
        print("⚠️ No se encontró botón escritorio. Probando login estilo móvil...")
        try:
            # Fallback al botón estilo móvil (con aria-label)
            login_btn = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//div[@role="button" and @aria-label="Iniciar sesión"]'))
            )
            login_btn.click()
        except Exception as e:
            print("❌ No se pudo hacer click en ningún botón de login.")
            raise e

    try:
        btn = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, f'//span[contains(text(), {"Guardar información" if guardar_info else "Ahora no"})]/ancestor::div[@role="button"]'))
        )
        btn.click()
    except:
        pass

    print("✅ Login exitoso con UI escritorio o fallback móvil.")

def login_instagram_movil(driver, username, password, guardar_info=False):
    print("🔄 Intentando login estilo móvil...")
    driver.get("https://www.instagram.com/accounts/login/")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "username")))

    driver.find_element(By.NAME, "username").clear()
    driver.find_element(By.NAME, "username").send_keys(username)
    driver.find_element(By.NAME, "password").clear()
    driver.find_element(By.NAME, "password").send_keys(password)

    try:
        login_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//div[@role="button" and @aria-label="Iniciar sesión"]'))
        )
        login_btn.click()
    except:
        print("⚠️ No se encontró botón móvil. Probando login escritorio...")
        try:
            # Botón estilo escritorio (más tradicional)
            login_btn = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//button[@type="submit"]'))
            )
            login_btn.click()
        except Exception as e:
            print("❌ No se pudo hacer click en ningún botón de login.")
            raise e

    try:
        btn = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, f'//span[contains(text(), {"Guardar información" if guardar_info else "Ahora no"})]/ancestor::div[@role="button"]'))
        )
        btn.click()
    except:
        pass

    print("✅ Login exitoso con UI móvil.")


