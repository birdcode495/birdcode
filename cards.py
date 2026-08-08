import streamlit as st


def iniciar_sesion():

	st.page_link('login.py', label = 'Inicia sesión o registrate', icon = ':material/login:')
	st.image('Images/Login3.png', width = 260, use_container_width = True)


def cargar_archivo_link():

	st.page_link('carga_archivo.py', label = 'Locate: Ubicación del Proyecto', icon = ':material/upload_file:')
	st.image('Images/Upload_file.png', width = 260, use_container_width = True)


def lista_especies():

	st.page_link('lista_especies.py', label = 'Evaluate & Assess: Diagnóstico', icon = ':material/local_florist:')
	st.image('Images/Eagle3.png', width = 270, use_container_width = True)


def especies_amenazadas():

	st.page_link('lista_especies_amenazadas.py', label = 'Prepare: Oportunidades de Crédito Verde', icon = ':material/star:')
	st.image('Images/Endangered_species.png', width = 240, use_container_width = True)