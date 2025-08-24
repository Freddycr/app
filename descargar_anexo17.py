
import requests
from datetime import datetime, timedelta

def descargar_anexo17():
    """
    Descarga el Anexo 17 desde el portal de OSINERGMIN para un rango de fechas.
    """
    # 1. Calcular las fechas
    fecha_fin_dt = datetime.now()
    fecha_inicio_dt = fecha_fin_dt - timedelta(days=15)

    # Formatear las fechas al formato YYYY-MM-DD
    formato_fecha = '%Y-%m-%d'
    fecha_inicio_str = fecha_inicio_dt.strftime(formato_fecha)
    fecha_fin_str = fecha_fin_dt.strftime(formato_fecha)

    # 2. Construir la URL
    url_base = "https://www.else.com.pe/PortalOsinergmin/Anexo17"
    params = {
        'CodigoAnexo': 4,
        'FechaInicio': fecha_inicio_str,
        'FechaFin': fecha_fin_str
    }
    
    # requests se encargará de codificar los parámetros correctamente en la URL
    url = f"{url_base}?CodigoAnexo={params['CodigoAnexo']}&FechaInicio={params['FechaInicio']}&FechaFin={params['FechaFin']}"

    print(f"Descargando datos desde: {url}")

    # 3. Descargar el archivo
    nombre_archivo = 'anexo17_osinergmin.xlsx'
    try:
        response = requests.get(url_base, params=params, timeout=30) # Timeout de 30 segundos
        response.raise_for_status()  # Lanza un error para respuestas no exitosas (ej. 404, 500)

        # Verificar que el contenido sea de un archivo excel
        if 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' in response.headers.get('Content-Type', ''):
            with open(nombre_archivo, 'wb') as f:
                f.write(response.content)
            print(f"Archivo '{nombre_archivo}' descargado exitosamente.")
        else:
            print("Error: La respuesta del servidor no es un archivo Excel.")
            print(f"Content-Type recibido: {response.headers.get('Content-Type')}")

    except requests.exceptions.RequestException as e:
        print(f"Error al descargar el archivo: {e}")

if __name__ == '__main__':
    descargar_anexo17()
