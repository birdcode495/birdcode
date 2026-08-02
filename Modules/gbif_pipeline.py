import geopandas as gpd
import pandas as pd
import streamlit as st
import shapely.wkt
from pygbif import occurrences as occ
from shapely.ops import orient


def obtener_occurrencias_gbif_directo_gdf(gdf, distancia_buffer_metros = 2000, max_registros = 10000):

	''' Recibe un Geodataframe directamente cargado en memoria, aplica un buffer métrico simplificado basado en la tipología del proyecto
	óptimo para la API de GBIF minimizando la densidad de vértices y limitando decimales para evitar el error 400, extrae su polígono,	
	lo formatea según las reglas estrictas de GBIF (CRS: 4326 y orientacion de la geometria en sentido contrareloj), 
	y descarga las ocurrencias

	'''

	if gdf is None or gdf.empty:

		return pd.DataFrame()

	try:

		# 1. PASO CRÍTICO: Reproyectar a coordenadas métricas oficiales de Colombia (EPSG:9377)
		# Esto permite aplicar el buffer en metros exactos, no en grados decimales.
		if gdf.crs != "EPSG:9377":

			gdf_metrico = gdf.to_crs("EPSG:9377")

		else:

			gdf_metrico = gdf

		# 2. Unificar geometrías y aplicar el buffer espacial parametrizado
		geometria_unida = gdf_metrico.unary_union
		poligono_buffer_metrico = geometria_unida.buffer(distancia_buffer_metros)

		# 3. EXTRA-DEFENSA: Calcular la envolvente convexa (Convex Hull) y SIMPLIFICAR
		# El método .simplify(10) reduce drásticamente la cantidad de puntos de la curva del buffer,
		# eliminando vértices innecesarios cada 10 metros para no saturar la URL de GBIF.
		poligono_simplificado = poligono_buffer_metrico.convex_hull.simplify(10)

		# 4. Reproyectar el polígono optimizado a WGS84 (EPSG:4326)
		gdf_wgs84 = gpd.GeoDataFrame(geometry = [poligono_simplificado], crs = 'EPSG:9377').to_crs('EPSG:4326')
		poligono_wgs84 = gdf_wgs84.geometry.iloc[0]

		# 5. Asegurar que la geometría resultante sea estrictamente un POLYGON
		# (Si por error de origen da un Point o Linestring tras simplificar, usamos su envelope)
		if poligono_wgs84.geom_type != 'Polygon':

			poligono_wgs84 = poligono_wgs84.envelope

		# 6. Forzar orientación contra-reloj (Counter-Clockwise) exigida por GBIF
		poligono_orientado = orient(poligono_wgs84, sign = 1.0)

		# 7. CONTROL DE PRECISIÓN Y DECIMALES (Evita URLs kilométricas que causan el error 400)
		# Limita los flotantes a un máximo de 5 posiciones decimales (~1.1 metros de precisión física)
		wkt_string = shapely.wkt.dumps(poligono_orientado, rounding_precision = 5)

		# Guardar en el estado para poder graficarlo después
		st.session_state['wkt_buffer_actual'] = wkt_string

		# ----------------------------------------------------------------------------------------------------------------------

		# IMPLEMENTACIÓN DE PAGINACIÓN AUTOMATIZADA

		# Targeted backend keys (GBIF internal class codes)

		# 212 - Aves, 131 - Amphibia, 359 - Mammalia, 7707728 - Tracheophyta (Vascular plants)
		clases_prioritarias = [212, 131, 359, 7707728]

		todos_los_registros = []
		limite_pagina = 300  # Máximo estricto permitido por la API de GBIF por llamada espacial
		# Marcador visual dinámico para la interfaz de Streamlit
		status_text = st.empty()


		# RUN SMART QUERIES BY TAXONOMIC TARGET GROUP

		for clase_id in clases_prioritarias:

			offset_actual = 0

			while True:

				status_text.text(f'Consulta del lado del servidor GBIF...Clave de clase: {clase_id} | Fila actual: {offset_actual})')

				# Server side optimization: Pass strict constraints inside the request
				# Realizar la llamada especificando la página de registros correspondientes 
				respuesta = occ.search(
					geometry = wkt_string,
					classKey = clase_id, # Core biological focus
					year = '2000,2026', # Eradicates pre-GPS historical noise instantly
					limit = limite_pagina,
					offset = offset_actual
				)

				registros_pagina = respuesta.get('results', [])
				conteo_total_clase = respuesta.get('count', 0) # El total real en los servidores de GBIF

				if not registros_pagina:

					break

				todos_los_registros.extend(registros_pagina)

				# Halt if we extracted all real occurrences for this specific class
				if len(registros_pagina) < limite_pagina or len(todos_los_registros) >= conteo_total_clase:

					break

				# Hard safely rail per class group to prevent RAM exhaustion
				if offset_actual >= max_registros:

					break


				# Desplazar el puntero para la siguiente página
				offset_actual = offset_actual + limite_pagina

		status_text.empty() # Limpiar el texto temporal

		if not todos_los_registros:

			return pd.DataFrame()

		df_completo = pd.DataFrame(todos_los_registros)
		#print(f'Total real en GBIF: {conteo_total_db} | Total descargado con éxito: {len(df_completo)}')
		return df_completo


	except Exception as e:

		# Esto capturará cualquier fallo e imprimirá un debug detallado en la interfaz de Streamlit
		st.error(f'Error técnico en el pipeline geográfico de GBIF: {e}')
		return pd.DataFrame()


		