import streamlit as st
from cards import cargar_archivo_link

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

