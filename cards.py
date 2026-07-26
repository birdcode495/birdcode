import streamlit as st


def iniciar_sesion():

	st.page_link('login.py', label = 'Inicia sesión o registrate', icon = ':material/login:')
	st.image('Images/Login3.png', width = 260, use_container_width = True)


def cargar_archivo_link():

	st.page_link('carga_archivo.py', label = 'Carga el archivo espacial de tu proyecto', icon = ':material/upload_file:')
	st.image('Images/Upload_file.png', width = 260, use_container_width = True)


def lista_especies():

	st.page_link('lista_especies.py', label = 'Consulta la lista de especies en tu proyecto', icon = ':material/local_florist:')
	st.image('Images/Eagle3.png', width = 270)


def especies_amenazadas():

	st.page_link('lista_especies_amenazadas.py', label = 'Especies amenazadas en tu proyecto', icon = ':material/star:')
	st.image('Images/Endangered_species.png', width = 240)