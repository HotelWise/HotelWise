from sys import argv
import logging
import json
import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.runners import DataflowRunner, DirectRunner
import polars as pl
import googlemaps

gmaps = googlemaps.Client(key='AIzaSyB9Sa4Myba6_qwXawPjjWWKVUEELVYZstk')

# Función para realizar transformaciones en el DataFrame de Pandas
def aplicar_transformaciones(beampc):
    lineas = beampc.split('\n')
    names = []
    gmap_id  = []
    descrptions  = []
    latitudes  = []
    longitudes  = []
    categories  = []
    avg_ratings  = []
    num_of_reviews   = []
    MISCs  = []
    urls  = []
    for linea in lineas:
        if linea.strip():  # Ignora líneas en blanco
            objeto_json = json.loads(linea)
            names.append(objeto_json['name'])
            gmap_id.append(objeto_json['gmap_id'])
            descrptions.append(objeto_json['description'])
            latitudes.append(objeto_json['latitude'])
            longitudes.append(objeto_json['longitude'])
            if objeto_json['category']:
                c=0
                for categoria in objeto_json['category']:
                    if 'hotel' in categoria.lower():
                        c+=1
                        categories.append(objeto_json['category'])
                        break
                if c == 0:
                    categories.append(None)
            else:
                categories.append(None)
            avg_ratings.append(objeto_json['avg_rating'])
            num_of_reviews.append(objeto_json['num_of_reviews'])
            servicios = []
            if (objeto_json['MISC'] != 'null') and (objeto_json['MISC'] != 'None') and objeto_json['MISC']:    
                for key,value in objeto_json['MISC'].items():
                    if (value != 'null') and (value != 'None') and value and key not in ['Health & safety', 'Planning']:
                        servicios.extend(value)
            else:
                servicios = None
            if servicios == []:
                servicios = None
            MISCs.append(servicios)
            urls.append(objeto_json['url'])
    data = {
    "name": names,
    "gmap_id": gmap_id,
    "descrption": descrptions,
    "latitude": latitudes,
    "longitude": longitudes,
    "category": categories,
    "avg_rating": avg_ratings,
    "num_of_reviews": num_of_reviews,
    "facilities": MISCs,
    "url": urls
    }
    df = pl.DataFrame(data)
    df = df.filter(~pl.col('category').is_null())
    df = df.unique(subset=['gmap_id'], keep='first')
    return df

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


# ### main

def run():
    # Command line arguments
    options = PipelineOptions(flags=argv)
    
    # Static input and output
    input = 'gs://hw-d1/raw-data/1.json'
    output = 'hotelwise-415022:dshw.hoteles'

    # Table schema for BigQuery
    table_schema = {
        "fields": [
            {
                "name": "name",
                "type": "STRING"
            },
            {
                "name": "gmap_id",
                "type": "STRING"
            },
            {
                "name": "description",
                "type": "STRING"
            },
            {
                "name": "latitude",
                "type": "FLOAT"
            },
            {
                "name": "longitude",
                "type": "FLOAT"
            },
            {
                "name": "category",
                "type": "STRING"
            },
            {
                "name": "avg_rating",
                "type": "FLOAT"
            },
            {
                "name": "num_of_reviews",
                "type": "INTEGER"
            },
            {
                "name": "facilities",
                "type": "STRING"
            },
            {
                "name": "url",
                "type": "STRING"
            },
            {
                "name": "County",
                "type": "STRING"
            },
            {
                "name": "City",
                "type": "STRING"
            },
            {
                "name": "State",
                "type": "STRING"
            },
            {
                "name": "Country",
                "type": "STRING"
            }
        ]
    }

    # Create the pipeline
    with beam.Pipeline(options=options) as pipeline:
        datos_pcollection = (
            pipeline
            | 'Cargar archivo json' >> beam.io.ReadFromText(input)
        )
        datos_transformados_pcollection = (
            datos_pcollection
            | 'Aplicar transformaciones' >> beam.Map(aplicar_transformaciones)
        )
        datos_geograficos_pcollection = (
            datos_transformados_pcollection
            | 'Obtener datos geograficos' >> beam.Map(obtener_geo)
        )
        datos_geograficos_pcollection| 'WriteToBQ' >> beam.io.WriteToBigQuery(
            output,
            schema=table_schema,
            create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED,
            write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND
            )
    logging.getLogger().setLevel(logging.INFO)
    logging.info("Building pipeline ...")

if __name__ == '__main__':
  run()
