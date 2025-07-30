from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import random

options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=options)
driver.get("https://calculadora-creditos-uva.streamlit.app/")

time.sleep(7)  # Esperar a que cargue la app

try:
    # Paso 1: Ingresar número aleatorio en el input
    number_input = driver.find_element(By.ID, "number_input_1")
    number_input.clear()
    number_input.send_keys(str(random.randint(10000, 500000)))

    time.sleep(1)  # Esperar que se registre el cambio

    # Paso 2: Clic en el botón "Calcular"
    button = driver.find_element(By.XPATH, "//button[.//p[text()='Calcular']]")
    button.click()

    time.sleep(3)  # Esperar a que procese
except:
    pass  # Silenciar errores

driver.quit()

