
import requests

def descargar_aviso_senamhi():
    """
    Descarga el archivo SHAPE-ZIP de avisos de 24H desde SENAMHI
    utilizando la URL directa del servicio geográfico.
    """
    # URL del servicio WFS (Web Feature Service) que genera el SHAPE-ZIP
    url = "https://idesep.senamhi.gob.pe/geoserver/g_prono_pp_24h/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=g_prono_pp_24h:view_aviso24h&maxFeatures=20000&outputFormat=SHAPE-ZIP"
    url = "https://idesep.senamhi.gob.pe/geoserver/g_prono_pp_24h/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=g_prono_pp_24h:view_aviso24h&maxFeatures=20000&outputFormat=SHAPE-ZIP"

    
    nombre_archivo = "senamhi_aviso24h.zip"

    print(f"Descargando archivo desde: {url}")

    try:
        # Realizar la petición GET a la URL
        # Se añade un timeout para evitar que el script se quede colgado indefinidamente
        response = requests.get(url, timeout=60)

        # Verificar si la petición fue exitosa (código de estado 200)
        response.raise_for_status()

        # Guardar el contenido de la respuesta en un archivo local
        with open(nombre_archivo, 'wb') as f:
            f.write(response.content)
        
        print(f"Archivo '{nombre_archivo}' descargado exitosamente.")

    except requests.exceptions.HTTPError as http_err:
        print(f"Error HTTP al intentar descargar el archivo: {http_err}")
    except requests.exceptions.ConnectionError as conn_err:
        print(f"Error de conexión: {conn_err}")
    except requests.exceptions.Timeout as timeout_err:
        print(f"La petición excedió el tiempo de espera: {timeout_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"Ocurrió un error inesperado al realizar la petición: {req_err}")

if __name__ == '__main__':
    descargar_aviso_senamhi()
