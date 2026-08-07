import os
import pandas as pd
import geopandas as gpd
from sqlalchemy import create_engine, text
import streamlit as st


def obtener_motor_supa():

	''' Establish a secure, SSL-encrypted connection pool to your cloud Supabase database'''
	DB_USER = 'postgres.wdlsaneeijnrjoliajcu'
	DB_PASSWORD = 'Nrisimhadeva_ajita_kali_888'
	DB_HOST = 'aws-0-ca-central-1.pooler.supabase.com'
	DB_PORT = '5432'
	DB_NAME = 'postgres'

	# MANDATORY BANKING SECURITY RULE: sslmode=require enforces extreme transit encryption
	url_conexion = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?sslmode=require'

	# Instantiate the SQLAlchemy engine pool
	engine = create_engine(url_conexion, echo = False)
	return engine


def cargar_dataframe_sesion_a_supabase(id_solicitud_banco):

	''' Extracts the raw/cleaned GBIF dataframe from st.session_state, normalizes spatial fields,
	and uploads it as an active spatial PostGIS table to Supabase'''

	# 1. Verification safeguard: pull the active dataset straight from global browser RAM
	if 'df_gbif_bruto' not in st.session_state or st.session_state['df_gbif_bruto'] is None:

		st.error('Ingestion failure: No active biodiversity dataset found in session memory')
		return None

	df_origen = st.session_state['df_gbif_bruto']

	if df_origen.empty:

		return None

	try:

		# Create a deep copy to prevent mutating the user's active session display matrix
		df_temp = df_origen.copy()

		# 2. DATA CLEANING AND RE-TYPING (Crucial to avoid PostgreSQL datatype crashes)
		# Convert any nested JSON dictionaries/lists from the GBIF API payload into basic strings
		for col in df_temp.columns:

			if df_temp[col].apply(lambda x: isinstance(x, (list, dict))).any():

				df_temp[col] = df_temp[col].astype(str)

		# 3. SPATIAL INTERPOLATION: Convert coordinates to a native GeoDataFrame
		# GBIF coordinates are natively stored in geographic WGS84 format (EPSG:4326)
		gdf_upload = gpd.GeoDataFrame(
			df_temp,
			geometry = gpd.points_from_xy(df_temp['decimalLongitude'], df_temp['decimalLatitude']),
			crs = 'EPSG:4326'
		)

		# Build an enterprise-safe isolated table name using the unique banking loan transaction ID
		nombre_tabla_destino = f'temp_analisis_{id_solicitud_banco}'

		# 4. EXECUTE CLOUD EXPORT VIA GEOALCHEMY
		engine = obtener_motor_supa()

		st.info(f'Connecting to Supabase Cloud Server...uploading {len(gdf_upload)} rows to table {nombre_tabla_destino}')

		# Geopandas generates the table infrastructure and PostGIS indices automatically
		gdf_upload.to_postgis(
			name = nombre_tabla_destino,
			con = engine,
			if_exists = 'replace', # Overwrite any stale, unclosed previous testing queries
			index = False
		)

		st.success(f'Data pipeline complete. Ingestion table {nombre_tabla_destino} is now fully queryable via SQL.')
		return nombre_tabla_destino

	except Exception as e:

		st.error(f'Error técnico durante el volcado de datos hacia Supabase: {e}')
		return None



def ejecutar_analisis_esg_postgis_aves(nombre_tabla_temp):

	''' Runs multi-layer relational queries inside Supabase to extract local threat metrics'''
	engine = obtener_motor_supa()

	query_sql = f'''

		SELECT
			DISTINCT g.species AS nombre_cientifico,
			g.order AS orden,
			g.family AS familia,
			assessments_iucn.red_list_category AS red_list_category,
			COUNT(DISTINCT key) AS registros

		FROM {nombre_tabla_temp} g
		LEFT JOIN assessments_iucn ON g.species = assessments_iucn.scientific_name
		WHERE g.species IS NOT NULL AND g.class = 'Aves'
		GROUP BY nombre_cientifico, orden, familia, red_list_category
		ORDER BY registros DESC;'''

	with engine.connect() as con:

		# Load the complete joined SQL result instantly into a fresh pandas table matrix
		df_esg_final = pd.read_sql_query(text(query_sql), con)

		# MANDATORY BANK SECURITY CLOSURE (No persistencia en disco NDA Rule)
		# Erase the transient spatial points completely from the cloud schema right after evaluation
		con.execute(text(f'DROP TABLE IF EXISTS {nombre_tabla_temp};'))
		con.commit()

	return df_esg_final 






