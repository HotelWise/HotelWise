from google.cloud import storage
import pandas as pd
from DB_FILES import *

def process_crime():
    client = storage.Client(project=project_id)
    bucket = client.bucket(bucket_name)

    crime_dataset = pd.read_parquet(
        f"gs://{bucket_name}/{file_crime_parquet}")
    hoteles_dataset = pd.read_parquet(
        f"gs://{bucket_name}/{file_hoteles_parquet}")

    # Realizar la fusión
    hoteles_final = pd.merge(hoteles_dataset, crime_dataset[['STATE', 'CITY', 'CRIME RATE']],
                             left_on=[hoteles_dataset['STATE'].str.lower(
                             ), hoteles_dataset['CITY'].str.lower()],
                             right_on=[crime_dataset['STATE'].str.lower(
                             ), crime_dataset['CITY'].str.lower()],
                             how='left')

    # Eliminar las columnas adicionales
    hoteles_final.drop(['key_0', 'key_1', 'CITY_y',
                       'STATE_y'], axis=1, inplace=True)
    hoteles_final.rename(
        columns={'CITY_x': 'CITY', 'STATE_x': 'STATE'}, inplace=True)

    hoteles_para_guardar = hoteles_final[['NAME', 'LATITUDE', 'LONGITUDE',
                                          'CITY', 'COUNTY', 'STATE', 'TEXT', 'AVG_RATING', 'CRIME RATE', 'AMENITIES']]
    hoteles_para_guardar.rename(
        columns={'TEXT': 'REVIEWS', 'CRIME RATE': 'CRIME_RATE'}, inplace=True)

    hoteles_para_guardar.to_parquet(
        f"gs://{bucket_name}/{file_hoteles_parquet_final}", index=False)

    print(
        f"Parquet file successfully uploaded to GCS: {file_hoteles_parquet_final}")
