import streamlit as st
import pandas as pd
from Modules.database import cargar_dataframe_sesion_a_supabase, ejecutar_analisis_esg_postgis_aves
from Modules.database import cargar_dataframe_sesion_a_supabase, ejecutar_analisis_esg_postgis_restricciones


st.header('Inteligencia avanzada para diagnósticos de biodiversidad')
aves, restricciones, dependencias, oportunidades = st.tabs([
	'Consulta de Aves', 'Riesgos de veda y hábitat', 'Dependencias de soporte', 'Oportunidades de crédito verde'])

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
					st.metric(label = 'Total especies de aves detectadas', value = len(df_esg_dashboard))
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
							),
						'gallery': st.column_config.LinkColumn(
							'Galería',
							display_text = 'Ver galería',
							help = 'Consulta a galería en GBIF'
							)
						},
						use_container_width = True,
						hide_index = True)



with restricciones:

	st.subheader('Diagnóstico de presencia de orquideas, mamíferos y plantas')

	if st.session_state.get('shp_cargado', False) and st.session_state['df_gbif_bruto'] is not None:

		# Establish an arbitrary corporate credit ID for tracking
		id_credito_actual = 'credito_bogota_2026_999'

		if st.button('Iniciar analisis de restricción territorial'):

			with st.spinner('Estableciendo tunel TLS seguro e ingiriendo datos vectoriales...'):

				# Step 1: Dump data from browser session memory to supabase
				tabla_generada = cargar_dataframe_sesion_a_supabase(id_solicitud_banco = id_credito_actual)

				if tabla_generada:

					# Step 2: Run the analytical PostGIS query layer and auto-drop tables
					with st.spinner('Ejecutando consultas de biodiversidad...'):

						df_esg_dashboard = ejecutar_analisis_esg_postgis_restricciones(tabla_generada)

					# Step 3: Print out the final database output
					st.subheader('Consolidado de estadísticas de biodiversidad emitido por el servidor PostgreSQL')
					st.metric(label = 'Total especies detectadas', value = len(df_esg_dashboard))
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
						
						# 2. STATISITICAL SPATIAL AGGREGATES
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
							),
						'gallery': st.column_config.LinkColumn(
							'Galería',
							display_text = 'Ver galería',
							help = 'Consulta a galería en GBIF'
							)
						},
						use_container_width = True,
						hide_index = True)

					# 0. ----
					st.info(f'''
						** Criterio técnico TNFD /ANLA **: Las alertas generadas a continuación evalúan la totalidad del área de influencia configurada ({st.session_state.get('ultima_distancia')} m).
						Según la legislación colombiana y el Estandar de Desempeño 6 de la IFC, los hallazgos bióticos dentro de este buffer conllevan las mismas obligaciones y restricciones legales que si se encontraran dentro del área estricta de operación.
						''')


					# 1. AUTOMATION PROCESS: CRITICAL LEGAL ALERT (Orchids)
					df_orquideas = df_esg_dashboard[df_esg_dashboard['familia'] == 'Orchidaceae']
					conteo_orquideas = len(df_orquideas)

					if conteo_orquideas > 0:

						st.error(f'''
							** ALERTA CRÍTICA: Bloqueo Legal por Veda Nacional de Flora**
							**Estatus**: Se detectó la presencia potencial de **{conteo_orquideas}** especies de la familia **Orchidaceae**.
							**Impacto Legal**: En Colombia, toda la flora epífita está cobijada por una Veda Nacional Obligatoria. El cliente no podrá iniciar obras civiles ni remoción de tierras sin tramitar un *Levantamiento de Veda* ante la ANLA.
							**Impacto Financiero**: Alta probabilidad de **retraso de 6 a 12 meses** en el cronograma operativo del proyecto. Riesgo moderado-alto de afectación al flujo de caja inicial para el pago de cuotas de crédito.
						''')

					# 2. AUTOMATION PROCESS: HIGH ESG RISK ALERT (IUCN Endangered / critical)
					categorias_amarillas = ['CR', 'EN', 'Critically Endangered', 'Endangered', 'VU', 'Vulnerable']

					df_amarillo = df_esg_dashboard[df_esg_dashboard['red_list_category'].str.contains('|'.join(categorias_amarillas), na = False)]
					conteo_amarillo = len(df_amarillo)

					if conteo_amarillo > 0:

						categorias_encontradas = df_amarillo['red_list_category'].unique()
						lista_categorias_str = ', '.join(categorias_encontradas)

						st.warning(f'''
							** ALERTA DE COMPLIANCE: Hábitat crítico Detectado (Estandar IFC 6 / Principios de Ecuador)**
							**Estatus**: Se detectó la presencia potencial de **{conteo_amarillo}** especies en categorias de alto riesgo de extinción según la Lista Roja de la IUCN (**{lista_categorias_str}**).
							**Impacto Internacional**: Satisface los criterios de activación de *Hábitat Crítico* bajo los Principios de Ecuador (EP4). El Banco se expone a riesgos de reputación e incumplimiento ESG si financia la destrucción de esta población sin compensación certificada.
							**Acción Requerida**: Condicionar los desembolsos de capital a la entrega de la Licencia Ambiental en firme y al Plan de Compensación de Biodiversidad con Ganancia Neta validado por la CAR local.
							''')

					# 3. AUTOMATION PROCESS: STANDARD MONITORING ALERT (Near Threatened)
					# Define tracking thresholds for low/medium vulnerability categories (Umbrella species)
					categorias_azules = ['NT', 'Near Threatened', 'Casi Amenazado']

					df_azul = df_esg_dashboard[df_esg_dashboard['red_list_category'].str.contains('|'.join(categorias_azules), na = False)]
					conteo_azul = len(df_azul)

					if conteo_azul > 0:

						st.info(f'''
							**NOTA DE MONITOREO**: Especies de alta sensibilidad ecológica (Especies Paraguas)**
							**Estatus**: Se detectó la presencia potencial de **{conteo_azul}** especies en categoría **Casi Amenazada (NT)** dentro del buffer de influencia.
							**Impacto Operativo**: No genera bloqueos regulatorios inmediatos, pero representa poblaciones altamente propensas a escalar en peligro si el diseño de ingeniería altera corredores de conectividad local.
							**Acción Requerida**: Requerir formalmente al cliente la inclusión de protocolos de ahuyentamiento de fauna y el diseño de pasos de fauna estructurados en sus Planes de Manejo Ambiental (PMA).
							''' )

					# If the system sweeps the dataset and finds absolutely zero risks, provide clear feedback to the user
					if conteo_orquideas == 0 and conteo_amarillo == 0 and conteo_azul == 0:

						st.success('**Cumplimiento Ambiental Inicial Satisfecho**: El área de influencia evaluada no presenta coincidencia de registros históricos con Vedas Nacionales de epífitas o Hábitats Críticos globales de la Lista Roja de la IUCN.')

				else:

					st.warning('Cargue un polígono e inicie el prediagnóstico para poblar la matriz automatizada de riesgos')




					

						
        			

       

        			
							
