#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 23 13:51:28 2025

@author: frdd
"""

import geopandas as gpd
# from sqlalchemy import create_engine, text

# --- 1. EXTRACT ---
# URL que devuelve el formato GeoJSON (usando 'application/json')
url = "https://idesep.senamhi.gob.pe/geoserver/g_prono_pp_24h/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=g_prono_pp_24h:view_aviso24h&maxFeatures=20000&outputFormat=application/json"

print("Descargando y leyendo datos geoespaciales...")
gdf = gpd.read_file(url)
print(f"Se leyeron {len(gdf)} registros.")

# --- 2. TRANSFORM ---
# El GeoDataFrame 'gdf' ya tiene los datos listos.
# La columna 'geometry' contiene los objetos geométricos.
# Creamos una nueva columna con la geometría en formato WKT para Oracle.
# El SRID 4326 es el estándar para WGS84.
gdf['geometry_wkt'] = gdf['geometry'].apply(lambda geom: geom.wkt)

# Preparamos el DataFrame para la carga, quitando la columna de geometría original
df_to_load = gdf.drop(columns=['geometry'])

# --- 3. LOAD ---
# Configura tu cadena de conexión a Oracle
# (reemplaza con tus credenciales)
# user = 'your_user'
# password = 'your_password'
# host = 'your_oracle_host'
# port = 1521
# service_name = 'your_service_name'
# dsn = f"{host}:{port}/{service_name}"

# engine = create_engine(f'oracle+oracledb://{user}:{password}@{dsn}')

table_name_staging = 'STAGING_PRONOSTICO'
table_name_final = 'FINAL_PRONOSTICO'

print(f"Cargando datos a la tabla de staging: {table_name_staging}...")
# Carga los datos a una tabla de staging (temporal)
# df_to_load.to_sql(
#     table_name_staging, 
#     engine, 
#     if_exists='replace', 
#     index=False,
#     chunksize=1000 # Importante para grandes volúmenes de datos
# )

print("Moviendo datos a la tabla final y convirtiendo geometría...")
# Usamos una transacción para mover los datos y convertir el WKT a SDO_GEOMETRY
# with engine.connect() as connection:
#     connection.execute(text(f"TRUNCATE TABLE {table_name_final}"))
#     connection.execute(text(f"""
#         INSERT INTO {table_name_final} (gid, nivel, nom_nivel, geometria_sdo)
#         SELECT 
#             gid, 
#             nivel, 
#             nom_nivel, 
#             SDO_GEOMETRY(geometry_wkt, 4326) -- Conversión clave
#         FROM {table_name_staging}
#     """))
#     connection.commit()

print("Proceso ETL completado exitosamente.")