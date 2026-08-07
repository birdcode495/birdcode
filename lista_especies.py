import streamlit as st
import pandas as pd
from Modules.database import cargar_dataframe_sesion_a_supabase, ejecutar_analisis_esg_postgis_aves


st.header('Inteligencia avanzada para diagnósticos de biodiversidad')
aves, aves_endemicas, mamiferos, plantas_vasculares, polinizadores, frutales_exoticos, orquideas = st.tabs([
	'Consulta de Aves', 'Aves endémicas', 'Mamíferos', 'Plantas vasculares', 'Polinizadores', 'Frutales exóticos', 'Orquideas'])

with aves:

	st.subheader('Diagnóstico de biodiversidad de aves en polígono consultado:')

	if st.session_state.get('shp_cargado', False) and st.session_state['df_gbif_bruto'] is not None:

		# Establish an arbitrary corporate credit ID for tracking
		id_credito_actual = 'credito_bogota_2026_99'

		if st.button('Iniciar analisis de riesgo territorial'):

			with st.spinner('Estableciendo tunel TLS seguro e ingiriendo datos vectoriales...'):

				# Step 1: Dump data from browser session memory to supabase
				tabla_generada = cargar_dataframe_sesion_a_supabase(id_solicitud_banco = id_credito_actual)

				if tabla_generada:

					# Step 2: Run the analytical PostGIS query layer and auto-drop tables
					with st.spinner('Ejecutando consultas de biodiversidad...'):

						df_esg_dashboard = ejecutar_analisis_esg_postgis_aves(tabla_generada)

					# Step 3: Print out the final database output
					st.subheader('Consolidado de estadísticas de biodiversidad emitido por el servidor PostgreSQL')
					st.dataframe(
						df_esg_dashboard,
						column_config = {
						# 1. TAXONOMIC IDENTIFIERS AND DESCRIPTORS
						'nombre_cientifico': st.column_config.TextColumn(
							'Nombre científico',
							help = 'Binomio taxonómico oficial validado por la API de GBIF'
							),
						'orden': st.column_config.TextColumn(
							'Orden',
							help = 'Clasificación taxonómica del orden biológico'
							),
						'familia': st.column_config.TextColumn(
							'Familia',
							help = 'Familia taxonómica correspondiente'
							),
						'red_list_category': st.column_config.TextColumn(
							'Categoría IUCN',
							help = 'Estado oficial de conservación global (CR, EN, VU, LC)'
							),
						# 2. MULTILINGUAL DICTIONARY MATRIX
						'nombre_comun': st.column_config.TextColumn(
							'co Nombre Común (ES)',
							help = 'Nombre común estandarizado en español según el catálogo IOC'
							),
						'english_name': st.column_config.TextColumn(
							'us English Name',
							help = 'Official standardized avian English identifier'
							),
						'chinese_name': st.column_config.TextColumn(
							'cn Chinese Name',
							help = 'Official avian identifier in chinese characters'
							),
						# 3. STATISITICAL SPATIAL AGGREGATES
						'registros': st.column_config.NumberColumn(
							'Conteo Registros',
							help = 'Número absoluto de ocurrencias geoespaciales detectadas dentro del buffer',
							format = '%d' # Displays as a clean integer without decimal points
							),
						'url_ficha': st.column_config.LinkColumn(
							'Ficha Técnica',
							display_text = 'Abrir ficha IUCN',
							help = 'Enlace externo verificado al perfil biológico de la especie'
							),
						'mapa': st.column_config.LinkColumn(
							'Rango Geográfico',
							display_text = 'Ver distribución',
							help = 'Consulta a mapa en formato JPG'
							)
						},
						use_container_width = True,
						hide_index = True)









# # 1. Check if the user has uploaded data first
# if not st.session_state['shp_cargado'] or st.session_state['df_gbif_bruto'] is None:

# 	st.warning('No se han encontrado datos en memoria. Por favor, cargue un archivo shapefile/KML/Geojson primero en la pestaña Cargar Archivo')

# else:

# 	# 2. Extract dataframe directly from browser global memory (Instant speed)
# 	df = st.session_state['df_gbif_bruto']

# 	if df.empty:

# 		st.info('No se encontraron registros biológicos dentro del polígono evaluado.')

# 	else:

# 		st.metric(label = 'Total ocurrencias históricas detectadas', value = len(df))

# 		st.subheader('Inventario de especies identificadas')
# 		st.write('A continuación se presentan los campos taxonómicos principales extraidos para la linea base: ')

# 		# 3. Select standard Darwin Core columns dynamically safely
# 		columnas_interes = ['scientificName', 'kingdom', 'class', 'family', 'basisOfRecord', 'year', 'coordinateUncertaintyInMeters']

# 		# Ensure columns exists in the database to prevent crashes
# 		columnas_existentes = [col for col in columnas_interes if col in df.columns]

# 		df_filtrado_vista = df[columnas_existentes]

# 		# Renaming columns for localized corporate presentation
# 		nombres_columnas = {
# 			'scientificName': 'Nombre cientifico',
# 			'kingdom': 'Reino',
# 			'class': 'Clase',
# 			'family': 'Familia',
# 			'basisOfRecord': 'Naturaleza del registro',
# 			'year': 'Año',
# 			'coordinateUncertaintyInMeters': 'Incertidumbre (m)'
# 		} 

# 		df_vista_bonita = df_filtrado_vista.rename(columns = nombres_columnas)

# 		# 4. Display clean interactively sortable tables
# 		st.dataframe(df_vista_bonita, use_container_width = True)

# 		# ready to pass this dataframe down into your custom data_cleaning or database modules!