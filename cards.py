import streamlit as st


def iniciar_sesion():

	st.page_link('login.py', label = 'Inicia sesión o registrate', icon = ':material/login:')
	st.image('Images/Login3.png', width = 260, use_container_width = True)


def cargar_archivo_link():

	st.page_link('carga_archivo.py', label = 'Carga el archivo espacial de tu proyecto', icon = ':material/upload_file:')
	st.image('Images/Upload_file.png', width = 260, use_container_width = True)