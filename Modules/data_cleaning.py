import pandas as pd
import geopandas as gpd


def depurar_inventario_gbif(df_raw, anio_corte_gps = 2000, incertidumbre_maxima = 2000):

	''' Aplies rigorous data validation to the raw GBIF dataframe using Pandas / Geopandas
	before transmitting data to the cloud database'''

	if df_raw is None or df_raw.empty:

		return pd.DataFrame()

	# Create a cpy to prevent SettingWithCopyWarning in Pandas
	df = df_raw.copy()

	initial_count = len(df)

	# 1. REMOVE DUPLICATES (Programmatic Deduplication)
	# Drops records with identical species found at the same coordinates on the same day
	columnas_duplicados = ['scientificName', 'decimalLatitude', 'decimalLongitude', 'eventDate']
	columnas_existentes = [col for col in columnas_duplicados if col in df.columns]
	df = df.drop_duplicates(subset = columnas_existentes, keep = 'first')

	# 2. DATA TYPE NORMALIZATION
	df['year'] = pd.to_numeric(df['year'], errors = 'coerce')
	df['coordinateUncertaintyInMeters'] = pd.to_numeric(df['coordinateUncertaintyInMeters'], errors = 'coerce')

	# 3. APPLY HYBRID GPS CUTOFF FILTER
	# Condition A: if uncertainty is documented, it must be under the threshold (e.g., 2000 m)
	condicion_incetidumbre_valida = df['coordinateUncertaintyInMeters'] <= incertidumbre_maxima

	# Condition B: if uncertainty is missing (NaN), only accept modern records (>= year 2000) 
	condicion_nulo_pero_moderno = df['coordinateUncertaintyInMeters'].isna() & (df['year'] >= anio_corte_gps)

	# Combine conditions to extract valid rows
	df_limpio = df[condicion_incetidumbre_valida | condicion_nulo_pero_moderno]

	# 4. EXCLUDE LOW QUALITY OBSERVATION BASES
	if 'basisOfRecord' in df_limpio.columns:

		excluir_basis = ['FOSSIL_SPECIMEN', 'LIVING_SPECIMEN']
		df_limpio = df_limpio[~df_limpio['basisOfRecord'].isin(excluir_basis)]

	final_count = len(df_limpio)
	print(f'Data cleaning complete: filtered out {initial_count - final_count} noise records')

	return df_limpio