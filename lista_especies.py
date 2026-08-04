import streamlit as st
import pandas as pd
from Modules.data_cleaning import depurar_inventario_gbif


st.header('Diagnóstico de Registros Biológicos (GBIF)')

# 1. Check if the user has uploaded data first
if not st.session_state['shp_cargado'] or st.session_state['df_gbif_bruto'] is None:

	st.warning('No se han encontrado datos en memoria. Por favor, cargue un archivo shapefile/KML/Geojson primero en la pestaña Cargar Archivo')

else:

	# 2. Extract dataframe directly from browser global memory (Instant speed)
	df = st.session_state['df_gbif_bruto']

	if df.empty:

		st.info('No se encontraron registros biológicos dentro del polígono evaluado.')

	else:

		st.metric(label = 'Total ocurrencias históricas detectadas', value = len(df))

		st.subheader('Inventario de especies identificadas')
		st.write('A continuación se presentan los campos taxonómicos principales extraidos para la linea base: ')

		# 3. Select standard Darwin Core columns dynamically safely
		columnas_interes = ['scientificName', 'kingdom', 'class', 'family', 'basisOfRecord', 'year', 'coordinateUncertaintyInMeters']

		# Ensure columns exists in the database to prevent crashes
		columnas_existentes = [col for col in columnas_interes if col in df.columns]

		df_filtrado_vista = df[columnas_existentes]

		# Renaming columns for localized corporate presentation
		nombres_columnas = {
			'scientificName': 'Nombre cientifico',
			'kingdom': 'Reino',
			'class': 'Clase',
			'family': 'Familia',
			'basisOfRecord': 'Naturaleza del registro',
			'year': 'Año',
			'coordinateUncertaintyInMeters': 'Incertidumbre (m)'
		} 

		df_vista_bonita = df_filtrado_vista.rename(columns = nombres_columnas)

		# 4. Display clean interactively sortable tables
		st.dataframe(df_vista_bonita, use_container_width = True)

		# ready to pass this dataframe down into your custom data_cleaning or database modules!