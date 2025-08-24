import time
import pandas as pd
import os
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

# --- Configuración Global ---
URL = "https://servicios.distriluz.com.pe/OsinergAnexo17/ReporteAnexo17.aspx"

# DataFrame con las empresas
EMPRESAS_DF = pd.DataFrame({
    'ede': ['ELNO', 'ELN', 'ELNM', 'ELC'],
    'empresa_id': ['1', '2', '3', '4']
})

# 1. Opciones de Chrome para la descarga automática y evitar bloqueos
OPTIONS = Options()
script_dir = os.path.dirname(os.path.abspath(__file__))
descargas_path = os.path.join(script_dir, "descargas_distriluz")

prefs = {
    "download.default_directory": descargas_path,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "plugins.always_open_pdf_externally": True,
    "safebrowsing.enabled": True,
    "safebrowsing.disable_download_protection": True
}
OPTIONS.add_experimental_option("prefs", prefs)
OPTIONS.add_argument("--no-sandbox")
OPTIONS.add_argument("--disable-extensions")
OPTIONS.add_argument("--disable-dev-shm-usage")

# 2. Ruta al chromedriver
ruta_chromedriver = '/home/frdd/Documentos/app/chromedriver/linux-139.0.7258.138/chromedriver-linux64/chromedriver'
SERVICE = Service(executable_path=ruta_chromedriver)

def descargar_reporte_para_empresa(empresa_nombre, empresa_id):
    """
    Abre una nueva sesión del navegador, descarga un reporte para una empresa
    y luego cierra la sesión. Esto aísla cada descarga.
    """
    print(f"--- Iniciando proceso para: {empresa_nombre} (ID: {empresa_id}) ---")
    driver = None # Definir driver como None al principio
    try:
        # Iniciar un nuevo driver para esta empresa
        driver = webdriver.Chrome(service=SERVICE, options=OPTIONS)
        
        driver.get(URL)

        # --- PASO 1: Seleccionar el tipo de reporte ---
        print("Seleccionando el tipo de reporte...")
        select_reporte = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "cboReporte"))
        )
        select_reporte.find_element(By.XPATH, '//option[@value="16"]').click()
        time.sleep(1)

        # --- PASO 2: Seleccionar la empresa ---
        print(f"Seleccionando la empresa {empresa_nombre}...")
        driver.find_element(By.ID, "cboEmpresa").find_element(
            By.XPATH, f'//option[@value="{empresa_id}"]').click()
        time.sleep(1)

        # --- PASO 3: Ingresar las fechas ---
        print("Ingresando fechas...")
        fecha_inicio_str = (datetime.now() - timedelta(days=30)).strftime('%d/%m/%Y')
        fecha_fin_str = datetime.now().strftime('%d/%m/%Y')

        driver.execute_script("arguments[0].value = arguments[1];",
                              driver.find_element(By.ID, "date_field"), fecha_inicio_str)
        driver.execute_script("arguments[0].value = arguments[1];",
                              driver.find_element(By.ID, "date_field1"), fecha_fin_str)
        time.sleep(0.5)

        # --- PASO 4: Hacer clic en el botón de descarga ---
        print("Haciendo clic en el botón de descarga...")
        driver.execute_script("arguments[0].click();",
                              driver.find_element(By.ID, "ImageButton1"))

        # Esperar un tiempo prudencial para que la descarga se complete
        print("Esperando a que la descarga finalice...")
        time.sleep(15) # Aumentamos un poco la espera por si acaso
        print(f"Proceso para {empresa_nombre} completado.")

    except Exception as e:
        print(f"Ocurrió un error inesperado durante el proceso de {empresa_nombre}: {e}")
    finally:
        if driver:
            # Cerrar el navegador para esta empresa
            driver.quit()
            print(f"Navegador para {empresa_nombre} cerrado.\n")

if __name__ == '__main__':
    # Asegurarse de que el directorio de descargas existe
    if not os.path.exists(descargas_path):
        print(f"Creando directorio de descargas en: {descargas_path}")
        os.makedirs(descargas_path)

    # --- Bucle principal ---
    # Llama a la función de descarga para cada una de las empresas
    for index, row in EMPRESAS_DF.iterrows():
        descargar_reporte_para_empresa(row['ede'], row['empresa_id'])
    
    print("--- Todos los procesos han finalizado. ---")