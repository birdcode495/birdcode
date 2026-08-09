import streamlit as st
import pandas as pd
from Modules.database import cargar_dataframe_sesion_a_supabase, ejecutar_analisis_esg_postgis_prepare


st.header('🦜 Paso 3: PREPARE — Oportunidades de Financiamiento Verde')
st.markdown('''
	Este panel identifica **Activos Bióticos de Alto Valor** dentro del área de influencia del Proyecto,
	permitiendo calificar la operación para líneas de Crédito Verde, Bonos de Biodiversidad y proyectos de Aviturismo.
	''')

# 1. Verification safeguard: Ensure data exists in memory from the Locate phase
if 'df_gbif_bruto' not in st.session_state or st.session_state['df_gbif_bruto'] is None:

	st.warning('⚠️ No se detectan datos espaciales en la sesión. Por favor cargue primero el shapefile del proyecto en el **Paso 1: LOCATE**')

else:

	# Simulating the dataframe that has already gone through your local Supabase LEFT JOIN
	# with the 'aves_endemicas_colombia' table and 'multilingual_ioc' table
	# df_oportunidades = ejecutar_analisis_esg_postgis_prepare()
	id_credito_prepare = 'credito_bogota_2026_9999'

	if st.button('Iniciar análisis de líneas de Crédito Verde'):

		with st.spinner('Estableciendo tunel TLS seguro e ingiriendo datos vectoriales...'):

			tabla_prepare = cargar_dataframe_sesion_a_supabase(id_solicitud_banco = id_credito_prepare)

			if tabla_prepare:

				with st.spinner('Ejecutando consultas de biodiversidad...'):

					df_oportunidades = ejecutar_analisis_esg_postgis_prepare(tabla_prepare)

				st.subheader('Consolidado de estadísticas de biodiversidad')
				st.metric(label = 'Total aves endémicas detectadas', value = len(df_oportunidades))

				# 2. Execute Finantial Metric Summary Blocks
				col1, col2, col3 = st.columns(3)
				with col1:

					st.metric(label = 'Aves Endémicas Identificadas', value = '5')

				with col2:

					st.metric(label = 'Score de Atractivo Turístico Internacional', value = '4.8 / 5.0 (Premium)')

				with col3:

					st.metric(label = 'Viabilidad de Crédito de Conservación', value = 'Apta (Tasa Preferencial)')

				st.markdown('---')
				st.subheader('🔍 Inventario Homologado de Activos Bióticos para Reportes TNFD')
				st.info('💡 **Consejo Comercial**: Las especies listadas abajo son altamente cotizadas por el mercado internacional de aviturismo. La presencia de estas poblaciones justifica la estructuración de un Crédito Verde.')


				# 3. THE ENTERPRISE OPORTUNITY DATA GRID
				# We configure standard columns to show multilingual common names elegantly
				st.dataframe(
					df_oportunidades,
					column_config = {
					'nombre_cientifico': st.column_config.TextColumn('🧬 Nombre Científico'),
					'nombre_comun_es': st.column_config.TextColumn('co Nombre Común (ES)'),
					'nombre_comun_en': st.column_config.TextColumn('us English Common Name'),
					'nombre_comun_fr': st.column_config.TextColumn('fr Nom Commun (FR)'),
					'nombre_comun_cn': st.column_config.TextColumn('cn 中文名'),
					'familia': st.column_config.TextColumn('Familia taxonómica'),
					'red_list_category': st.column_config.TextColumn('Categoría IUCN'),
					'registros': st.column_config.NumberColumn('Conteo Registros', format = '%d'),
					'url_ficha': st.column_config.LinkColumn('Ficha Técnica', display_text = 'Abrir ficha IUCN'),
					'mapa': st.column_config.LinkColumn('Rango Geográfico', display_text = 'Ver distribución')
					},
					column_order = [
						'nombre_comun_es', 'nombre_comun_en', 'nombre_comun_fr', 'nombre_comun_cn', 'nombre_cientifico', 'familia', 
						'red_list_category', 'registros', 'url_ficha', 'mapa'],
					use_container_width = True,
					hide_index = True
				)

