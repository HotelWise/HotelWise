import apache_beam as beam
import json
import polars as pl
import googlemaps
from ufunc import udf
import subprocess

comando = "gsutil cp gs://hw-d1/gmk/APK.txt /APK"
subprocess.run(comando, shell=True)

archivo_entrada = 'gs://hw-d1/raw-data/1.json'
archivo_salida = 'gs://hw-d1/clean-data/1.parquet'

with open('./APK/APK.txt', 'r') as file:
    api_key = file.read().strip()

gmaps = googlemaps.Client(key=api_key)

with beam.Pipeline() as pipeline:
    # Carga el archivo json como una PCollection de Polars DataFrames
    datos_pcollection = (
        pipeline
        | 'Cargar archivo json' >> beam.Create([archivo_entrada])
        | 'Convertir a DataFrame de Polars' >> beam.Map(udf.cargar_archivo_json)
    )

    # Aplica transformaciones utilizando Polars
    datos_transformados_pcollection = (
        datos_pcollection
        | 'Aplicar transformaciones' >> beam.Map(udf.aplicar_transformaciones)
    )
    # Aplica transformaciones utilizando Polars
    datos_geograficos_pcollection = (
        datos_transformados_pcollection
        | 'Obtener datos geograficos' >> beam.Map(udf.obtener_geo)
    )
    # guarda el resultado
    datos_geograficos_pcollection | 'Guardar datos transformados' >> beam.Map(lambda df: df.write_parquet(archivo_salida))