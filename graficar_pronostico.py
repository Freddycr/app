import geopandas as gpd
import matplotlib.pyplot as plt
import contextily as ctx

# --- 1. EXTRACT ---
# URL que devuelve el formato GeoJSON (usando 'application/json')
url = "https://idesep.senamhi.gob.pe/geoserver/g_prono_pp_24h/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=g_prono_pp_24h:view_aviso24h&maxFeatures=20000&outputFormat=application/json"

print("Descargando y leyendo datos geoespaciales...")
try:
    # Leemos los datos geoespaciales directamente desde la URL
    gdf = gpd.read_file(url)
    print(f"Se leyeron {len(gdf)} registros.")
except Exception as e:
    print(f"No se pudo descargar o leer el archivo desde la URL. Error: {e}")
    exit()

# --- 2. PLOT ---
if not gdf.empty:
    print("Generando el gráfico con mapa base...")
    
    try:
        # Reproyectar los datos al sistema de coordenadas de los mapas web (Web Mercator)
        # para que los datos y el mapa base coincidan.
        gdf_web = gdf.to_crs(epsg=3857)

        # Crear la figura y los ejes para el gráfico
        fig, ax = plt.subplots(1, 1, figsize=(15, 15))
        
        # Graficamos nuestros polígonos con algo de transparencia para ver el mapa de fondo
        gdf_web.plot(column='nivel', ax=ax, legend=True, cmap='viridis', alpha=0.6,
                     legend_kwds={'title': "Nivel de Peligro", 'loc': 'upper left'})

        # Añadimos el mapa base de OpenStreetMap usando contextily
        ctx.add_basemap(ax, source=ctx.providers.OpenStreetMap.Mapnik)

        # Añadimos un título al gráfico
        ax.set_title('Pronóstico de Peligro por Precipitaciones (24h) - SENAMHI', fontsize=16)
        
        # Ocultamos los ejes X e Y, ya que no son representativos en esta proyección
        ax.set_axis_off()

        # Mostramos el gráfico final
        print("Mostrando el gráfico. Cierra la ventana del gráfico para finalizar el script.")
        plt.show()

    except KeyError:
        # Este bloque se ejecuta si la columna 'nivel' no existe en los datos
        print("\nError: La columna 'nivel' no fue encontrada en los datos descargados.")
        print(f"Columnas disponibles: {gdf.columns.to_list()}")
        print("Por favor, revisa la lista y modifica el script para usar el nombre de columna correcto en la función gdf.plot().")

else:
    print("No se encontraron datos para graficar.")

print("Proceso completado.")