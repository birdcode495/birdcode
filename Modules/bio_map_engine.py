import os
import streamlit as st
import geopandas as gpd
import folium
from streamlit_folium import st_folium
from sqlalchemy import create_engine, text
from Modules.database import obtener_motor_supa



@st.cache_data(show_spinner = False)

def descargar_geometria_traslape_ram(nombre_tabla_temp, nombre_tabla_temp2) -> gpd.GeoDataFrame:

	''' Descarga exclusivamente los polígonos de la capa maestra que se intersecan
	con el buffer del cliente. Evita sobrecargar la RAM al no descargar toda la capa nacional'''

	engine = obtener_motor_supa()

	query = (f'''

		SELECT c.id, c.nombre, ST_AsEWKB(c.geom) AS geom_bytes
		FROM public.{nombre_tabla_temp} c
		WHERE ST_Intersects(c.geom, (SELECT ST_Union(geometry) FROM public.{nombre_tabla_temp2}))
		''')

	try:

		with engine.connect() as conn:

			df = pd.read_sql(query, conn)

		if df.empty:

			return gpd.GeoDataFrame()

		# Reconstrucción de la geometría en memoria volatil desde bytes EWKB

		gdf = gpd.GeoDataFrame(df, geometry = gpd.array.from_ewkb(df['geom_bytes'].values), crs = 'EPSG:4326')

		return gdf.drop(columns = ['geom_bytes'])

	except Exception:

		return gpd.GeoDataFrame()


#def generar_mapa_interactivo_tnfd()



