import geopandas as gpd
import pandas as pd
from pygbif import occurrences as occ
from shapely.ops import orient


def obtener_occurrencias_gbif_directo_gdf(gdf, max_registros = 100000):

	''' Recibe un Geodataframe directamente cargado en memoria, extrae su polígono,
	lo formatea según las reglas estrictas de GBIF, y descarga las ocurrencias

	'''
	# 1. Asegurar que el CRS sea WGS84 (Requisito obligatorio de GBIF)
	if gdf.crs != 'EPSG:4326':

		gdf = gdf.to_crs('EPSG:4326')

	# 2. Combinar geometrías en caso de que el cliente tenga múltiples polígonos
	geometria_unida = gdf.unary_union

	# Extraer polígono único o usar envolvente convexa para simplificar la consulta URL
	if geometria_unida.geom_type == 'MultiPolygon':

		poligono = geometria_unida.convex_hull

	else:

		poligono = geometria_unida


	# 3. regla crítica de GBIF: orientar los vertices en sentido contrareloj (counter-clockwise)
	poligono_orientado = orient(poligono, sign = 1.0)

	# 4. Generar el string WKT (Well-Known Text)
	wkt_string = poligono_orientado.wkt

	# 5. Consultar la API de GBIF usando pygbif
	try:

		resultados_crudos = occ.search(

			geometry = wkt_string,
			limit = max_registros
			)

		registros = resultados_crudos.get('results', [])

		if not registros:

			return pd.DataFrame() # Retorna dataframe vacío si no hay registros

		df_gbif = pd.DataFrame(registros)

		return df_gbif

	except Exception as e:

		error = 'Error al conectar con la API de GBIF: ', e
		return pd.DataFrame()

