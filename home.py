import streamlit as st
from cards import iniciar_sesion, cargar_archivo_link, lista_especies


col_init1, col_init2 = st.columns([2,1])


with col_init1:

	welcome = st.empty()
	welcome.header('Explorador de BirdCode')


with col_init2:

	st.image('Images/Eagle3.png', width = 70)


cols = st.columns(2)

with cols[0].container(height = 310):

	iniciar_sesion()

with cols[1].container(height = 310):

	cargar_archivo_link()

with cols[0].container(height = 310):

	lista_especies()

# with cols[1].container(height = 310):

# 	cryptography()

# with cols[0].container(height = 310):

# 	messaging()

# with cols[1].container(height = 310):

# 	digital_signature()

