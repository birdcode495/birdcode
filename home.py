import streamlit as st
from cards import cargar_archivo_link


col_init1, col_init2 = st.columns([2,1])


with col_init1:

	welcome = st.empty()
	welcome.header('Explorador de BirdCode App')


with col_init2:

	st.image('Images/Eagle.png', width = 70)


cols = st.columns(2)

with cols[0].container(height = 310):

	cargar_archivo_link()

# with cols[1].container(height = 310):

# 	social_engineering()

# with cols[0].container(height = 310):

# 	hashing()

# with cols[1].container(height = 310):

# 	cryptography()

# with cols[0].container(height = 310):

# 	messaging()

# with cols[1].container(height = 310):

# 	digital_signature()

