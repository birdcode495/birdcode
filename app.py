import streamlit as st


# Initialize the data frames and state markers
if 'df_gbif_bruto' not in st.session_state:

	st.session_state['df_gbif_bruto'] = None

if 'shp_cargado' not in st.session_state:

	st.session_state['shp_cargado'] = False

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
		title = 'Carga tu archivo',
		icon = ':material/upload_file:'
		),
	st.Page(
		'lista_especies.py',
		title = 'Lista de especies',
		icon = ':material/local_florist:'
		),
	st.Page(
		'lista_especies_amenazadas.py',
		title = 'Lista de especies amenazadas',
		icon = ':material/star:'
		),
	st.Page(
		'mapa.py',
		title = 'Mapa de distribución',
		icon = ':material/public:'
		),
	st.Page(
		'informe.py',
		title = 'Descarga informe',
		icon = ':material/analytics:'
		)


]


page = st.navigation(pages)
page.run()


with st.sidebar.container(height=310):

    if page.title == 'Home':

        st.page_link("home.py", label = 'Home')

    elif page.title == 'Login':

    	st.page_link('login.py', label = 'Login')

    elif page.title == 'Carga tu archivo':

        st.page_link("carga_archivo.py", label = 'Carga tu archivo')

    elif page.title == 'Lista de especies':

        st.page_link('lista_especies.py', label = 'Lista de especies')

    elif page.title == 'Lista de especies amenazadas':

        st.page_link('lista_especies_amenazadas.py', label = 'Lista de especies amenazadas')

    elif page.title == 'Mapa de distribución':

        st.page_link('mapa.py', label = 'Mapa de distribución')

    elif page.title == 'Descarga informe':

        st.page_link('informe.py', label = 'Descargar informe')

    
