import streamlit as st
import io
import geopandas as gpd
from Modules.gbif_pipeline import obtener_occurrencias_gbif_directo_gdf


col_init1, col_init2 = st.columns([2,1])
with col_init1:

    welcome = st.empty()
    welcome.header('Prediagnóstico automatizado de biodiversidad')


with col_init2:

    st.image('Images/Eagle4.png', width = 100)

uploaded_files = st.file_uploader("Suba el archivo .zip de su shapefile o archivo Geojson/KML: ",  
    type=['zip', 'geojson', 'kml', ]
)

if uploaded_files is not None:

    # 1. Read input in the UI layer
    bytes_data = io.BytesIO(uploaded_files.read())
    gdf_cliente = gpd.read_file(bytes_data)

    # 2. Call the backend processing module safely
    with st.spinner('Consultando la API de GBIF en tiempo real...'):
        df_bruto = obtener_occurrencias_gbif_directo_gdf(gdf_cliente)

    if not df_bruto.empty:

        st.success(f'Análisis completado para {len(df_bruto)} registros válidos')
        st.write('Muestra del conjunto de datos (10 registros)')
        st.dataframe(df_bruto[['gbifID','acceptedScientificName','kingdom','class']].head(10))



