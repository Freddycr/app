
import pandas as pd
import requests
import os
from datetime import datetime, timedelta

def descargar_datos_sismicos():
    """
    Descarga datos sísmicos desde el IGP y los guarda en un archivo Excel.
    """
    # Fechas
    hoy = datetime.now()
    ayer = hoy - timedelta(days=1)
    fecha_inicio = ayer.strftime('%d-%m-%Y')
    fecha_fin = hoy.strftime('%d-%m-%Y')

    # Coordenadas y otros parámetros (usando los de tu ejemplo)
    lat_min = -25.701
    lat_max = -1.396
    lon_min = -87.382
    lon_max = -65.624
    mag_min = 1
    mag_max = 9
    prof_min = 0
    prof_max = 900
    profundidad = 900

    # Construir la URL
    url = f"https://www.igp.gob.pe/servicios/centro-sismologico-nacional/datos-sismicos-xls/{fecha_inicio}/{fecha_fin}/{lat_min}/{lat_max}/{lon_min}/{lon_max}/{mag_min}/{mag_max}/{prof_min}/{prof_max}/{profundidad}"

    print(f"Descargando datos desde: {url}")

    # Descargar el archivo
    try:
        response = requests.get(url)
        response.raise_for_status()  # Lanza un error para respuestas no exitosas
        with open('datos-sismicos-igp.xlsx', 'wb') as f:
            f.write(response.content)
        print("Archivo 'datos-sismicos-igp.xlsx' descargado exitosamente.")
        return 'datos-sismicos-igp.xlsx'
    except requests.exceptions.RequestException as e:
        print(f"Error al descargar el archivo: {e}")
        return None

def combinar_con_historicos(nuevo_archivo, archivo_historico):
    """
    Combina los datos nuevos con un archivo histórico de datos sísmicos,
    asegurando que no haya duplicados.
    """
    if nuevo_archivo is None:
        print("No se pudo descargar el nuevo archivo, no se puede combinar.")
        return

    try:
        df_nuevo = pd.read_excel(nuevo_archivo)
        print(f"Leídos {len(df_nuevo)} registros del archivo nuevo.")

        # Si no hay datos nuevos, no es necesario hacer nada más con el histórico.
        if df_nuevo.empty:
            print("No hay registros nuevos para agregar.")
            return

        # Limpiar nombres de columnas (eliminar espacios al inicio/final)
        df_nuevo.columns = df_nuevo.columns.str.strip()

        try:
            df_historico = pd.read_excel(archivo_historico)
            print(f"Leídos {len(df_historico)} registros del archivo histórico '{archivo_historico}'.")
            df_historico.columns = df_historico.columns.str.strip()
            df_combinado = pd.concat([df_historico, df_nuevo], ignore_index=True)
        except FileNotFoundError:
            print(f"Archivo histórico '{archivo_historico}' no encontrado. Se creará uno nuevo.")
            df_combinado = df_nuevo

        # --- Validación de Duplicados ---
        columna_fecha = 'fecha UTC'
        if columna_fecha not in df_combinado.columns:
            print(f"Error: La columna '{columna_fecha}' no se encontró.")
            print(f"Las columnas disponibles son: {list(df_combinado.columns)}")
            return

        registros_antes = len(df_combinado)
        df_combinado.drop_duplicates(subset=[columna_fecha], keep='last', inplace=True)
        registros_despues = len(df_combinado)

        duplicados_eliminados = registros_antes - registros_despues
        if duplicados_eliminados > 0:
            print(f"Validación: Se encontraron y eliminaron {duplicados_eliminados} registros duplicados.")
        else:
            print("Validación: No se encontraron registros duplicados.")

        # Guardar el archivo combinado
        df_combinado.to_excel(archivo_historico, index=False)
        print(f"Datos combinados y guardados en '{archivo_historico}'. Total de registros ahora: {len(df_combinado)}")

    except Exception as e:
        print(f"Ocurrió un error al procesar los archivos: {e}")


if __name__ == '__main__':
    # Nombre del archivo que contendrá los datos históricos
    # Puedes cambiarlo si lo deseas.
    ARCHIVO_HISTORICO = 'historico_sismos.xlsx'

    # 1. Descargar los datos de hoy
    archivo_descargado = descargar_datos_sismicos()

    # 2. Combinar con los datos históricos
    if archivo_descargado:
        combinar_con_historicos(archivo_descargado, ARCHIVO_HISTORICO)
        # 3. Limpiar el archivo descargado
        try:
            os.remove(archivo_descargado)
            print(f"Archivo temporal '{archivo_descargado}' eliminado.")
        except OSError as e:
            print(f"Error al eliminar el archivo temporal: {e}")
