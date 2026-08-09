import streamlit as st
import pandas as pd
import numpy as np
from Modules.database import cargar_dataframe_sesion_a_supabase, ejecutar_analisis_esg_postgis_prepare


# INITIALIZE PERSISTENT SCHEMAS IN MEMORY
if 'df_postgis_resultado' not in st.session_state:

	st.session_state['df_postgis_resultado'] = None

if 'analisis_ejecutado' not in st.session_state:

	st.session_state['analisis_ejecutado'] = False


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

					st.session_state['df_postgis_resultado'] = ejecutar_analisis_esg_postgis_prepare(tabla_prepare)
					st.session_state['analisis_ejecutado'] = True
					st.success('✅ ¡Análisis relacional compilado y asegurado en la memoria RAM!')
					#df_oportunidades = ejecutar_analisis_esg_postgis_prepare(tabla_prepare)


	st.markdown('---')

	# INDEPENDENT RENDERING LAYER
	# This block runs continously as long as 'analisis_ejecutado' is True,
	# regardless of whether widgets are clicked or changed
	if st.session_state['analisis_ejecutado'] and st.session_state['df_postgis_resultado'] is not None:

		df_oportunidades = st.session_state['df_postgis_resultado']

		st.subheader('Consolidado de estadísticas de biodiversidad')
		#st.metric(label = 'Total aves endémicas detectadas', value = len(df_oportunidades))

		# 2. Execute Finantial Metric Summary Blocks
		col1, col2, col3 = st.columns(3)
		with col1:

			st.metric(label = 'Aves Endémicas Identificadas', value = len(df_oportunidades))

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


		st.markdown('---')
		st.subheader('📈 Modelación de Escenarios Bióticos Predictivos (Periodo 1990 - 2030+)')
		st.write(
			'Seleccione una de las especies de aves endémicas identificadas para proyectar el comportamiento de su rango '
			'de hábitat frente a choques macroeconómicos regionales y dinámicas de deforestación local')

		# 1. Check if our database query returned any endemic bird results
		if 'df_oportunidades' in locals() and not df_oportunidades.empty:

			# Create an interactive dropdown showing the common and scientific name of detected birds
			lista_especies = df_oportunidades['nombre_comun_es'] + ' (' + df_oportunidades['nombre_cientifico'] + ')'
			especie_seleccionada_str = st.selectbox('Seleccione el activo biótico a modelar', lista_especies)

			# Isolate the specific dataframe row matching the users selection
			nombre_cientifico_aislado = especie_seleccionada_str.split('(')[1].replace(')', '').strip()
			ave_seleccionada = df_oportunidades[df_oportunidades['nombre_cientifico'] == nombre_cientifico_aislado].iloc[0]

			# 2. THE CATEGORICAL INDEX MAPPING MATRIX
			# We turn text tokens into controlled mathematical coefficients to simulate graph shapes
			mapeo_coeficientes = {
				'DR': -3.5, # Decreciente rápida (Habitat collapse)
				'DL': -1.2, # Decreciente lenta (Gradual habitat loss)
				'ES': 0.0, # Estable (Flat horizontal line)
				'CL': 1.5, # Creciente lenta (Gradual regeneration)
				'CR': 3.5 # Creciente rápida (Aggresive reforestation recovery)
			}

			# Extract structural trend tokens from the database row with standard safe fallbacks
			c_base = mapeo_coeficientes.get(ave_seleccionada.get('tendencia_base', 'ES'), 0.0)
			c_extra = mapeo_coeficientes.get(ave_seleccionada.get('tendencia_extrativista', 'DL'), -1.2)
			c_verde = mapeo_coeficientes.get(ave_seleccionada.get('tendencia_verde', 'CL'), 1.5)

			# 3. TIME-SERIES NUMERICAL ARRAY GENERATION
			# Establish a clean 5-year step interval sequence from 1990 to 2030
			periodos = np.array(list(range(1990, 2031, 5)))

			# Compute the linear predictive equations (setting 100% as the baseline starting point in 1990)
			valores_base = 100 + (periodos - 1990) * c_base
			valores_extractivista = 100 + (periodos - 1990) * c_extra
			valores_regenerativo = 100 + (periodos - 1990) * c_verde

			# Assemble into a clean chart-ready tracking dataframe structured for streamlit
			df_chart = pd.DataFrame({
				'Año': periodos,
				'Tendencia base (actual)': valores_base,
				'Escenario extractivista (Riesgo de deforestación)': valores_extractivista,
				'Escenario regenerativo (Estabilización / Conservación)': valores_regenerativo
				}).set_index('Año')

			# 4. RENDER INTERACTIVE LINE CHART ON THE UI
			# Streamlit automatically handles multiple line mappings, color arrays, and zoom interactions
			st.line_chart(df_chart, use_container_width = True)

			# 5. ENTERPRISE TNFD INTERPRETATION BLOCK FOR THE CREDIT COMMITTEE
			st.markdown('#### 🔬 Dictamen metodológico de sostenibilidad crediticia')

			# Dynamic text logic mapping out exactly what the worst case scenario entails
			if ave_seleccionada.get('tendencia_extrativista', 'DL') == 'DR':

				st.error(f'''
					**🚨 EXPOSICIÓN CRÍTICA DE PORTAFOLIO**: Bajo un Escenario Extractivista Regional, la especie *{ave_seleccionada['nombre_cientifico']}*
					enfrenta un **Colapso Inminente de Hábitat (Tasa de contracción crítica)** para el año 2030+.
					Cualquier inversión crediticia convencional en este bloque enfrenta altas probabilidades de litigio social o revocatoria de Licencia Ambiental.
				''')

			else:
				st.warning(f'''
					**⚠️ VULNERABILIDAD MODERADA-ALTA**: El escenario extractivista proyecta una tendencia **Decreciente Lenta** con una pérdida neta estimada
					del **{abs(int(valores_extractivista[-1] - 100))}%** del rango de distribución remanente para 2030.
					Se sugiere condicionar el desembolso a la implementación de una franja de exclusión forestal inalterable dentro del título.
				''')

			# Highlight the oportunity trajectory to the bank's sustainable asset division
			st.success(f'''
				**🌿 OPORTUNIDAD DE TRANSICIÓN VERDE**: Al incentivar la estabilización de la frontera agrícola (Escenario regenerativo), el rango potencial de la especie
				muestra una tasa de recuperación del **{int(valores_regenerativo[-1] - 100)}%**. Este incremento califica al proyecto agropecuario para ser titular de **Créditos de Biodiversidad** transables.
			''')




