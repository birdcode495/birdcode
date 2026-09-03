import os
import streamlit as st
import geopandas as gpd
import folium
from streamlit_folium import st_folium
from sqlalchemy import create_engine, text
from Modules.database import obtener_motor_supa



@st.cache_data(show_spinner = False)

def descargar_geometria_traslape_ram(nombre_tabla_temp):

	''' Descarga exclusivamente los polígonos de la capa maestra que se intersecan
	con el buffer del cliente. Evita sobrecargar la RAM al no descargar toda la capa nacional'''

	engine = obtener_motor_supa()

	query = (f'''

		SELECT c.id, c.nombre, ST_AsEWKB(c.geom) AS geom_bytes
		FROM public.{nombre_tabla_temp} c
		WHERE ST_Intersects(c.geom, (SELECT ST_Union(geometry) FROM public.)))


