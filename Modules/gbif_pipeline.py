import geopandas as gpd
import pandas as pd
import streamlit as st
from pygbif import occurrences as occ
from shapely.ops import orient


def obtener_occurrencias_gbif_directo_gdf(gdf, distancia_buffer_metros = 2000, max_registros = 100000):

	''' Recibe un Geodataframe directamente cargado en memoria, aplica un buffer métrico basado en la tipología del proyecto,
	extrae su polígono,	lo formatea según las reglas estrictas de GBIF (CRS: 4326 y orientacion de la geometria en sentido contrareloj), 
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

		# 3. Simplificar a ConvexHull si el área resultante es un multipolígono complejo
		# Esto evita generar strings WKT gigantescos que rompan los límites de la URL de la API
		if poligono_buffer_metrico.geom_type == "MultiPolygon":

			poligono_final = poligono_buffer_metrico.convex_hull

		else:

			poligono_final = poligono_buffer_metrico

		# 4. Reproyectar de vuelta a WGS84 (EPSG:4326) obligatorio para GBIF
		gdf_wgs84 = gpd.GeoDataFrame(geometry = [poligono_final], crs = "EPSG:9377").to_crs("EPSG:4326")
		poligono_wgs84 = gdf_wgs84.geometry.iloc[0]

		# 5. Regla obligatoria GBIF: orientar vértices en sentido contra-reloj (Counter-clockwise)
		poligono_orientado = orient(poligono_wgs84, sign = 1.0)
		wkt_string = poligono_orientado.wkt

		# Guardar el WKT generado en la sesión para que otras páginas puedan dibujar el área del buffer
		st.session_state['wkt_buffer_actual'] = wkt_string

		# 6. Consultar la API de GBIF en tiempo real
		resultados_crudos = occ.search(

			geometry = wkt_string,
			limit = max_registros
		)

		registros = resultados_crudos.get('results', [])

		if not registros:

			return pd.DataFrame()

		return pd.DataFrame(registros)


	except Exception as e:

		st.error(f'Error técnico en el pipeline geográfico de GBIF: {e}')
		return pd.DataFrame()


