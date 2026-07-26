import streamlit as st


col_init1, col_init2 = st.columns([2,1])
with col_init1:

    welcome = st.empty()
    welcome.header('Carga el archivo de tu proyecto')


with col_init2:

    st.image('Images/Eagle4.png', width = 100)

uploaded_files = st.file_uploader("Cargar ficheros", accept_multiple_files="directory", 
    type=['geojson', 'kml', 'dbf', 'cpg', 'prj', 'shp', 'shx', 'gpkg']
)
# for uploaded_file in uploaded_files:
#     st.image(uploaded_file)