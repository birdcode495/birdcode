import streamlit as st
import io
import geopandas as gpd
from Modules.gbif_pipeline import obtener_occurrencias_gbif_directo_gdf
from Modules.data_cleaning import depurar_inventario_gbif
from Modules.database import cargar_dataframe_sesion_a_supabase, ejecutar_motor_alertas_tnfd 


l1, l2, l3, l4 = st.tabs(['L1: Huella empresarial', 'L2: Interfaz con la naturaleza', 'L3: Ubicación prioritaria', 
    'L4: Identificación del sector'])


with l1:

    col_init1, col_init2 = st.columns([2,1])
    with col_init1:

        welcome = st.empty()
        welcome.header('Carga de Proyectos e Infraestructura de Crédito')
        #st.write('Cargue los polígonos del Proyecto a financiar para calcular el área de influencia indirecta')


    with col_init2:

        st.image('Images/Eagle4.png', width = 100)


    st.markdown("""
        <style>
        [role=radiogroup] {
            gap: 1.5rem; 
        }
        </style>
    """, unsafe_allow_html=True)

    # Tu radio normal
    opcion_proyecto = st.radio("Elige una opción:", ['Pequeño impacto (Construcción local / Agricultura menor - Buffer: 1000 m)', 
        'Mediano impacto (Vías / Lineas de transmisión / Minería mediana - Buffer: 2000 m)', 
        'Alto impacto (Macro-minería / Hidrocarburos / Agroindustria pesada - Buffer: 5000 m)'],
        index = 1
        )

    # Asignación de la distancia métrica según la selección del analista de riesgo
    if '1000 m' in opcion_proyecto:

        distancia_buffer = 1000

    elif '2000 m' in opcion_proyecto:

        distancia_buffer = 2000

    else:

        distancia_buffer = 5000


    st.write('')
    uploaded_files = st.file_uploader("Suba el archivo .zip de su shapefile o archivo Geojson/KML: ",  
        type=['zip', 'geojson', 'kml', ]
    )

    if uploaded_files is not None:

        try:

            # 1. Read shapefile into memory layer
            bytes_data = io.BytesIO(uploaded_files.read())
            gdf_cliente = gpd.read_file(bytes_data)

            st.success(f'Geometría leida correctamente ({len(gdf_cliente)} polígonos).')

            # 2. RUN PIPELINE ONLY ONCE: Check if it was already processed to avoid re-running on widget clicks
            if st.session_state['df_gbif_bruto'] is None:

                with st.spinner('Consultando la API de GBIF en tiempo real...'):
                    # Execute your query module
                    df_bruto, df_pol = obtener_occurrencias_gbif_directo_gdf(gdf_cliente, distancia_buffer)

                # Clean data instantly in memory using GeoPandas / Pandas logic
                with st.spinner('Ejecutando algoritmos de depuración geoespacial en memoria...'):
                    df_limpio = depurar_inventario_gbif(df_bruto, anio_corte_gps = 2000, incertidumbre_maxima = 2000)

                    # SAVE DIRECTLY TO SESSION STATE
                    st.session_state['df_gbif_bruto'] = df_limpio
                    st.session_state['shp_cargado'] = True
                    st.session_state['ultima_distancia'] = distancia_buffer
                    st.session_state['df_buffer_cliente'] = df_pol
                    st.success(f'Datos descargados e indexados en memoria con éxito para {len(df_bruto)} registros válidos')
                    st.success(f'Datos limpiados con éxito para {len(df_limpio)} registros depurados')

                    if not df_limpio.empty:

                        #st.success(f'Análisis completado para {len(df_bruto)} registros válidos')
                        st.write('Muestra del conjunto de datos (20 registros)')
                        st.dataframe(df_limpio.head(20))
                        st.success(f'Se aplicó un buffer o área de influencia sobre el polígono cargado de: {distancia_buffer} metros')


            # Propose navigating to the next page smoothly
            st.info('Vaya a la pestaña ** Lista de especies ** en la barra lateral para ver los análisis.')

        except Exception as e:

            st.error(f'Error al procesar el archivo geoespacial: {e}')


    # Option to reset memory state if they want to upload a new file
    if st.session_state['shp_cargado']:

        if st.button('Limpiar memoria para cargar otro proyecto'):

            st.session_state['df_gbif_bruto'] = None
            st.session_state['shp_cargado'] = False
            st.session_state['df_buffer_cliente'] = False
            st.rerun()


with l2:

    st.subheader('🔴 Con qué biomas y ecosistemas interactuan estas actividades')



