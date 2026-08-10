import pandas as pd
import geopandas as gpd


def generar_tabla_audit_localidades(df_cleaned, top_n = 25):

	'''
	Groups clean GBIF session ocurrences into highly structure named
	locality blocks ranked by total sampling intensity and threat levels.
	'''
	if df_cleaned is None or df_cleaned.empty:

		return pd.DataFrame()

	df = df_cleaned.copy()

	if 'decimallatitude' not in df.columns or 'decimallongitude' not in df.columns:
		return pd.DataFrame()


	# Standardize threat tracking fields for counting
	df['red_list_category'] = df['iucnredlistcategory'].astype(str).str.strip().str.upper()
	threat_tokens = ['CR', 'EN', 'VU', 'CRITICALLY ENDANGERED', 'ENDANGERED', 'VULNERABLE']
	df['es_amenazada'] = df['red_list_category'].str.contains('|'.join(threat_tokens), na = False)



	# # 1. Spatial grid standardization (rounding coordinates to ~1.1 Km accuracy)
	# # This completely eliminates string fragmentation noise
	# df['lat_grid'] = df['decimallatitude'].round(2)
	# df['lon_grid'] = df['decimallongitude'].round(2)

	# 2. Execute aggregation loops
	def procesar_grupo(group):

		# Extract the most descriptive named locality string available inside this 1 Km grid block
		nombre_localidad = 'Coordenadas Exactas (Sin Nombre Registrado)'
		
		if 'locality' in group.columns:

			valid_names = group['locality'].dropna().astype(str).str.strip()
			# Filtered out generic short names like 'Colombia' or 'Valle del Cauca'
			valid_names = valid_names[valid_names.str.len() > 3]
			
			if not valid_names.empty:

				nombre_localidad = valid_names.value_counts().index[0] # Pick the most common string

		lat_centro_grid = group['decimallatitude'].iloc[0].round(2)
		lon_centro_grid = group['decimallongitude'].iloc[0].round(2)


		# # --- THE SOLUTON FIX ---
        # # Calculate the rounded grid center directly inside the group slice context.
        # # This completely bypasses the parent container generation race condition.
        # lat_centro_grid = group['decimallatitude'].iloc[0].round(2)
        # lon_centro_grid = group['decimallongitude'].iloc[0].round(2)


		return pd.Series({
			'Localidad Detectada': nombre_localidad,
			'Registros Totales (Avistamientos)': len(group),
			'Riqueza de Especies Únicas': group['species'].nunique() if 'species' in group.columns else group['scientificname'].nunique(),
			'Especies Amenazadas (CR/EN/VU)': group[group['es_amenazada']]['species'].nunique() if 'species' in group.columns else group[group['es_amenazada']]['scientificname'].nunique(),
			'Latitud': lat_centro_grid,
			'Longitud': lon_centro_grid

			})

	# Group by spatial blocks
	df_localidades = df.groupby(
		[df['decimallatitude'].round(2), df['decimallongitude'].round(2)], as_index = False).apply(procesar_grupo)

	if df_localidades.empty:

		return pd.DataFrame()

	# Rank the table by total sampling volume to show the highest-intensity hotspots first
	df_ranking = df_localidades.sort_values(by = 'Registros Totales (Avistamientos)', ascending = False)

	return df_ranking