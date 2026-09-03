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
			geometry = gpd.points_from_xy(df_temp['decimallongitude'], df_temp['decimallatitude']),
			crs = 'EPSG:4326'
		)

		#gdf_upload.columns = gdf_upload.columns.str.lower()

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



# ---------------------------------------------------------

def cargar_dataframe_pol_sesion_a_supabase(id_solicitud_banco, id_solicitud_banco2):

	# 1. Verification safeguard: pull the active dataset straight from global browser RAM
	if 'df_buffer_cliente' not in st.session_state or st.session_state['df_buffer_cliente'] is None:

		st.error('Ingestion failure: No active biodiversity dataset found in session memory')
		return None

	df_origen_pol = st.session_state['df_buffer_cliente']
	df_crudo_pol = st.session_state['df_crudo_pol_cliente']

	# if df_origen_pol.empty:

	# 	return None

	try:

		# Create a deep copy to prevent mutating the user's active session display matrix
		df_temp = df_origen_pol
		df_temp_pol_crudo = df_crudo_pol

		# 2. DATA CLEANING AND RE-TYPING (Crucial to avoid PostgreSQL datatype crashes)
		# Convert any nested JSON dictionaries/lists from the GBIF API payload into basic strings
		# for col in df_temp.columns:

		# 	if df_temp[col].apply(lambda x: isinstance(x, (list, dict))).any():

		# 		df_temp[col] = df_temp[col].astype(str)

		

		# Build an enterprise-safe isolated table name using the unique banking loan transaction ID
		nombre_tabla_destino = f'temp_analisis_{id_solicitud_banco}'
		nombre_tabla_destino_pol_crudo = f'temp_analisis_pol_crudo_{id_solicitud_banco2}'

		gdf_temp = gpd.GeoDataFrame(geometry = [df_temp], crs = 'EPSG:9377')
		gdf_temp_pol_crudo = gdp.GeoDataFrame(geometry = [df_temp_pol_crudo])

		# 4. EXECUTE CLOUD EXPORT VIA GEOALCHEMY
		engine = obtener_motor_supa()

		st.info(f'Connecting to Supabase Cloud Server...uploading rows to table {nombre_tabla_destino}')

		# Geopandas generates the table infrastructure and PostGIS indices automatically
		gdf_temp.to_postgis(
			name = nombre_tabla_destino,
			con = engine,
			if_exists = 'replace', # Overwrite any stale, unclosed previous testing queries
			index = False
		)

		gdf_temp_pol_crudo.to_postgis(
			name = nombre_tabla_destino_pol_crudo,
			con = engine,
			if_exists = 'replace',
			index = False
		)

		st.success(f'Procesamiento de datos completado.La tabla {nombre_tabla_destino} está disponible ahora para realizar consultas SQL.')
		return nombre_tabla_destino, nombre_tabla_destino_pol_crudo

	except Exception as e:

		st.error(f'Error técnico durante el volcado de datos hacia Supabase: {e}')
		return None




def ejecutar_analisis_esg_postgis_aves(nombre_tabla_temp):

	''' Runs multi-layer relational queries inside Supabase to extract local threat metrics'''
	engine = obtener_motor_supa()

	query_sql = f'''

		SELECT
			DISTINCT g.species AS nombre_cientifico,
			g.kingdom AS kingdom,
			g.class AS class,
			g.order AS orden,
			g.family AS familia,
			assessments_iucn.red_list_category AS red_list_category,
			COUNT(DISTINCT key) AS registros,

			-- Dynamic SQL URL generation (Consumes zero database disk space)
			'https://www.iucnredlist.org/species/' || assessments_iucn.internal_taxon_id || '/' || assessments_iucn.assessment_id AS url_ficha,
			'https://www.iucnredlist.org/api/v4/assessments/' || assessments_iucn.assessment_id || '/distribution_map/jpg' AS mapa
			
		FROM {nombre_tabla_temp} g
		LEFT JOIN assessments_iucn ON g.species = assessments_iucn.scientific_name
		WHERE g.species IS NOT NULL AND assessments_iucn.red_list_category <> 'Least Concern' 
		AND assessments_iucn.red_list_category <> 'Data Deficient' AND assessments_iucn.red_list_category <> 'Lower Risk/least concern'
		GROUP BY nombre_cientifico, kingdom, class, orden, familia, red_list_category, url_ficha, mapa
		ORDER BY registros DESC;'''

	with engine.connect() as con:

		# Load the complete joined SQL result instantly into a fresh pandas table matrix
		df_esg_final = pd.read_sql_query(text(query_sql), con)
		#st.write('Columnas crudas entregadas por SQL', list(df_esg_final.columns))

		# MANDATORY BANK SECURITY CLOSURE (No persistencia en disco NDA Rule)
		# Erase the transient spatial points completely from the cloud schema right after evaluation
		con.execute(text(f'DROP TABLE IF EXISTS {nombre_tabla_temp};'))
		con.commit()

	return df_esg_final



def ejecutar_analisis_esg_postgis_restricciones(nombre_tabla_temp):

	''' Runs multi-layer relational queries inside Supabase to extract local threat metrics'''
	engine = obtener_motor_supa()

	query_sql = f'''

		SELECT
			DISTINCT g.species AS nombre_cientifico,
			g.order AS orden,
			g.family AS familia,
			assessments_iucn.red_list_category AS red_list_category,
			COUNT(DISTINCT key) AS registros,

			-- Dynamic SQL URL generation (Consumes zero database disk space)
			'https://www.iucnredlist.org/species/' || assessments_iucn.internal_taxon_id || '/' || assessments_iucn.assessment_id AS url_ficha,
			'https://www.iucnredlist.org/api/v4/assessments/' || assessments_iucn.assessment_id || '/distribution_map/jpg' AS mapa

		FROM {nombre_tabla_temp} g
		LEFT JOIN assessments_iucn ON g.species = assessments_iucn.scientific_name
		WHERE g.species IS NOT NULL AND (g.family = 'Orchidaceae' OR g.class = 'Mammalia' OR g.kingdom = 'Plantae')
		GROUP BY nombre_cientifico, orden, familia, red_list_category, url_ficha, mapa
		ORDER BY registros DESC;'''

	with engine.connect() as con:

		# Load the complete joined SQL result instantly into a fresh pandas table matrix
		df_esg_restricciones = pd.read_sql_query(text(query_sql), con)
		#st.write('Columnas crudas entregadas por SQL', list(df_esg_final.columns))

		# MANDATORY BANK SECURITY CLOSURE (No persistencia en disco NDA Rule)
		# Erase the transient spatial points completely from the cloud schema right after evaluation
		con.execute(text(f'DROP TABLE IF EXISTS {nombre_tabla_temp};'))
		con.commit()

	return df_esg_restricciones


def ejecutar_analisis_esg_postgis_prepare(nombre_tabla_temp):

	''' Runs multi-layer relational queries inside Supabase to extract local threat metrics'''
	engine = obtener_motor_supa()

	query_sql2 = f'''

		SELECT
			DISTINCT g.species AS nombre_cientifico,
			multilingual_ioc.spanish AS nombre_comun_es,
			multilingual_ioc.english AS nombre_comun_en,
			multilingual_ioc.french AS nombre_comun_fr,
			multilingual_ioc.chinese AS nombre_comun_cn,
			g.family AS familia,
			aves_endemicas.categoria_iucn AS red_list_category,
			COUNT(DISTINCT key) AS registros,

			-- Dynamic SQL URL generation (Consumes zero database disk space)
			'https://www.iucnredlist.org/species/' || assessments_iucn.internal_taxon_id || '/' || assessments_iucn.assessment_id AS url_ficha,
			'https://www.iucnredlist.org/api/v4/assessments/' || assessments_iucn.assessment_id || '/distribution_map/jpg' AS mapa,

			-- Pulling the categorical scenario tokens from your endemic reference schema
			aves_endemicas.tendencia_base AS tendencia_base,
			aves_endemicas.tendencia_extractivista AS tendencia_extrativista,
			aves_endemicas.tendencia_verde AS tendencia_verde

		FROM {nombre_tabla_temp} g
		INNER JOIN aves_endemicas
			ON LOWER(TRIM(g.species)) = LOWER(TRIM(aves_endemicas.especie))
		LEFT JOIN multilingual_ioc 
			ON g.species = multilingual_ioc.species
		LEFT JOIN assessments_iucn
			ON g.species = assessments_iucn.scientific_name
		WHERE g.class = 'Aves'
		GROUP BY 1,2,3,4,5,6,7,9,10,11,12,13
		ORDER BY 8 DESC;'''

	with engine.connect() as con:

		# Load the complete joined SQL result instantly into a fresh pandas table matrix
		df_esg_prepare = pd.read_sql_query(text(query_sql2), con)
		#st.write('Columnas crudas entregadas por SQL', list(df_esg_final.columns))

		# MANDATORY BANK SECURITY CLOSURE (No persistencia en disco NDA Rule)
		# Erase the transient spatial points completely from the cloud schema right after evaluation
		con.execute(text(f'DROP TABLE IF EXISTS {nombre_tabla_temp};'))
		con.commit()

	return df_esg_prepare


def ejecutar_motor_alertas_tnfd(nombre_tabla_temp):

	engine = obtener_motor_supa()

	query_alertas = f'''

		SELECT

			-- DISTINCT g.species AS nombre_cientifico,
			-- g.family AS familia,
			--- Interseccion con paramos (MinAmbiente)
			EXISTS (
				SELECT 1 FROM paramos p
				WHERE ST_Intersects(g.geometry, p.geom)
			) AS en_paramo,
			-- Interseccion con RUNAP (areas protegidas)
			EXISTS (
				SELECT 1 FROM runap r
				WHERE ST_Intersects(g.geometry, r.geom)
			) AS en_runap,
			-- Interseccion con reservas forestales de la Ley 2 de 1959
			EXISTS (
				SELECT 1 FROM reservas_ley_2da_9377 l
				WHERE ST_Intersects(g.geometry, l.geom)
			) AS en_ley2,
			-- Interseccion con humedales ramsar
			EXISTS (
				SELECT 1 FROM humedales_ramsar h
				WHERE ST_Intersects(g.geometry, h.geom)
			) AS en_ramsar

		FROM {nombre_tabla_temp} g;'''


	with engine.connect() as con:

		# Load the complete joined SQL result instantly into a fresh pandas table matrix
		df_esg_traslape = pd.read_sql_query(text(query_alertas), con)
		#st.write('Columnas crudas entregadas por SQL', list(df_esg_final.columns))

		# MANDATORY BANK SECURITY CLOSURE (No persistencia en disco NDA Rule)
		# Erase the transient spatial points completely from the cloud schema right after evaluation
		#con.execute(text(f'DROP TABLE IF EXISTS {nombre_tabla_temp};'))
		con.commit()

	return df_esg_traslape



def calcular_areas_traslape_saras(nombre_tabla_temp):

	engine = obtener_motor_supa()

	query_traslapes = (f'''

		WITH usuario_proyectado AS (

			SELECT

				ST_Transform(geometry, 9377) AS geom_9377,
				ST_Area(ST_Transform(geometry, 9377)) / 10000.0 AS area_total_ha

			FROM {nombre_tabla_temp}
			LIMIT 1
		),

		calculo_paramos AS (
			
			SELECT

				'🔴 Páramo (MinAmbiente)'::text AS capa_ambiental,
				COALESCE(SUM(ST_Area(ST_Intersection(u.geom_9377, c.geom)) / 10000.0), 0.0) AS area_traslape_ha

			FROM usuario_proyectado u, paramos c
			WHERE ST_Intersects(u.geom_9377, c.geom)

		),
		calculo_runap AS (

			SELECT

				'🔴 RUNAP (Áreas Protegidas)'::text AS capa_ambiental,
				COALESCE(SUM(ST_Area(ST_Intersection(u.geom_9377, c.geom)) / 10000.0), 0.0) AS area_traslape_ha

			FROM usuario_proyectado u, runap c
			WHERE ST_Intersects(u.geom_9377, c.geom)
		),

		calculo_ramsar AS (

			SELECT

				'🔴 Humedal Ramsar'::text AS capa_ambiental,
				COALESCE(SUM(ST_Area(ST_Intersection(u.geom_9377, c.geom)) / 10000.0), 0.0) AS area_traslape_ha

			FROM usuario_proyectado u, humedales_ramsar c
			WHERE ST_Intersects(u.geom_9377, c.geom)
		),

		calculo_ley2 AS (

			SELECT

				'🟡 Reserva Forestal Ley 2'::text AS capa_ambiental,
				COALESCE(SUM(ST_Area(ST_Intersection(u.geom_9377, c.geom)) / 10000.0), 0.0) AS area_traslape_ha

			FROM usuario_proyectado u, reservas_ley_2da_9377 c
			WHERE ST_Intersects(u.geom_9377, c.geom)
		),

		unificado AS (

			SELECT * FROM calculo_paramos
			UNION ALL SELECT * FROM calculo_runap
			UNION ALL SELECT * FROM calculo_ramsar
			UNION ALL SELECT * FROM calculo_ley2

		)
		
		SELECT

			u.area_total_ha AS area_total_proyecto_ha,
			un.capa_ambiental,
			un.area_traslape_ha,

			CASE
				WHEN u.area_total_ha > 0 THEN (un.area_traslape_ha / u.area_total_ha) * 100.0
				ELSE 0.0

			END AS porcentaje_traslape

		FROM unificado un, usuario_proyectado u

	''')


	with engine.connect() as con:

		# Load the complete joined SQL result instantly into a fresh pandas table matrix
		df_esg_calculo_traslape = pd.read_sql_query(text(query_traslapes), con)
		#st.write('Columnas crudas entregadas por SQL', list(df_esg_final.columns))

		# MANDATORY BANK SECURITY CLOSURE (No persistencia en disco NDA Rule)
		# Erase the transient spatial points completely from the cloud schema right after evaluation
		con.execute(text(f'DROP TABLE IF EXISTS {nombre_tabla_temp};'))
		con.commit()

	return df_esg_calculo_traslape







