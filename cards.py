import streamlit as st


def cargar_archivo_link():

	st.page_link('login.py', label = 'Inicia sesión o registrate', icon = ':material/login:')
	st.image('Images/Login.png', width = 290, use_container_width = True)