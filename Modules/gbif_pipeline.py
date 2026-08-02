import geopandas as gpd
import pandas as pd
import streamlit as st
import shapely.wkt
from pygbif import occurrences as occ
from shapely.ops import orient


def obtener_occurrencias_gbif_directo_gdf(gdf, distancia_buffer_metros = 2000, max_registros = 100000):

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


		# 8. Consultar la API de GBIF en tiempo real
		resultados_crudos = occ.search(
			geometry = wkt_string,
			limit = max_registros
		)

		registros = resultados_crudos.get('results', [])

		if not registros:

			return pd.DataFrame

		return pd.DataFrame(registros)


	except Exception as e:

		# Esto capturará cualquier fallo e imprimirá un debug detallado en la interfaz de Streamlit
		st.error(f'Error técnico en el pipeline geográfico de GBIF: {e}')
		return pd.DataFrame()


		