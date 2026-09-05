import streamlit as st


# Initialize the data frames and state markers
if 'df_gbif_bruto' not in st.session_state:

	st.session_state['df_gbif_bruto'] = None

if 'shp_cargado' not in st.session_state:

	st.session_state['shp_cargado'] = False

if 'df_buffer_cliente' not in st.session_state:

	st.session_state['df_buffer_cliente'] = None

if 'df_crudo_pol_cliente' not in st.session_state:

	st.session_state['df_crudo_pol_cliente'] = None

# Initialize widget memory key
# We set the default text to match the 2000 meters option
# if 'buffer_seleccionado' not in st.session_state:

# 	st.session_state['buffer_seleccionado'] = 'Mediano impacto (Vías / Lineas de transmisión / Minería mediana - Buffer: 2000 m)'

# define the multi-page views
pages = [
	st.Page(
		'home.py',
		title = 'Home',
		icon = ':material/home:'
		),
	st.Page(
		'login.py',
		title = 'Login',
		icon = ':material/login:'
		),
	st.Page(
		'carga_archivo.py',
		title = 'Paso 1: Localizar',
		icon = ':material/upload_file:'
		),
	st.Page(
		'lista_especies.py',
		title = 'Paso 2: Evaluar & Analizar',
		icon = ':material/local_florist:'
		),
	st.Page(
		'prepare.py',
		title = 'Paso 3: Preparar',
		icon = ':material/star:'
		),
	st.Page(
		'mapa.py',
		title = 'Mapa de Distribución Geoespacial',
		icon = ':material/public:'
		),
	st.Page(
		'informe.py',
		title = 'Informe de Cumplimiento TNFD',
		icon = ':material/analytics:'
		)


]


page = st.navigation(pages)
page.run()


with st.sidebar.container(height=310):

    if page.title == 'Home':

        st.page_link("home.py", label = 'Home')
        st.write('Por medio de esta página de inicio puedes navegar a las distintas secciones de la App BirdCode')

    elif page.title == 'Login':

    	st.page_link('login.py', label = 'Login')

    elif page.title == 'Paso 1: Localizar':

        st.page_link("carga_archivo.py", label = 'LEAP: Locate')

    elif page.title == 'Paso 2: Evaluar & Analizar':

        st.page_link('lista_especies.py', label = 'Evaluate & Assess')

    elif page.title == 'Paso 3: Preparar':

        st.page_link('prepare.py', label = 'Prepare')

    elif page.title == 'Mapa de Distribución Geoespacial':

        st.page_link('mapa.py', label = 'Mapa de distribución')

    elif page.title == 'Informe de Cumplimiento TNFD':

        st.page_link('informe.py', label = 'Descargar informe')

    
