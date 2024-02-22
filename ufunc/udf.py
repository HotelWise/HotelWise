import json
import polars as pl
import googlemaps

with open('./APK/APK.txt', 'r') as file:
    api_key = file.read().strip()

gmaps = googlemaps.Client(key=api_key)

# Función para cargar un archivo JSON y convertirlo en un DataFrame de Pandas
def cargar_archivo_json(archivo):
    data_list=[]
    with open(archivo, 'r') as file:
        for line in file:
            # Cargar cada objeto JSON por separado
            data = json.loads(line)
            data_list.append(data)

    # Ahora data_list es una lista que contiene todos los objetos JSON del archivo
    df = pl.DataFrame(data_list)
    return df

# Función para realizar transformaciones en el DataFrame de Pandas
def aplicar_transformaciones(dft):
    dft = dft.drop(['address', 'description', 'price', 'hours', 'MISC', 'state', 'relative_results'])
    dft = dft.explode('category')
    dft = dft.filter(dft['category'].str.contains(f'(?i)hotel'))
    dft = dft.unique(subset=['gmap_id'], keep='first')
    return dft

# Definir la función para obtener city y country a partir de coordenadas
def obtener_geo(df2):
    counties, cities, states, countries, = [], [], [], []

    for lat, lon in zip(df2['latitude'], df2['longitude']):
        resultado = gmaps.reverse_geocode((lat, lon))
        county, city, state, country = None, None, None, None

        if resultado:
            for component in resultado[0]['address_components']:
                if 'locality' in component['types'] and not city:
                    city = component['long_name']

                elif 'administrative_area_level_2' in component['types'] and not county:
                    county = component['long_name']

                elif 'administrative_area_level_1' in component['types'] and not state:
                    state = component['long_name']

                elif 'country' in component['types'] and not country:
                    country = component['long_name']
                elif city and county and state and country:
                  break

        counties.append(county)
        cities.append(city)
        states.append(state)
        countries.append(country)

    counties, cities, states, countries = pl.Series(counties), pl.Series(cities), pl.Series(states), pl.Series(countries)
    df2 = df2.with_columns(
    County=counties,
    City=cities,
    State=states,
    Country=countries)
    return df2

