import pyarrow as pa 
import pyarrow.parquet as pq
import pandas as pd
from DB_FILES import *

hoteles_dataset_NLP = pd.read_parquet(f"gs://{bucket_name}/{file_hoteles_NLP_parquet}")

def extract_amenities():
    amenidades_sin_repetir = []
    for amenidades_str in hoteles_dataset_NLP['AMENITIES']:
        for amenidad in amenidades_str:
            if amenidad not in amenidades_sin_repetir:
                amenidades_sin_repetir.append({'AMENITIE':amenidad})

    amenidades_df = pd.DataFrame(amenidades_sin_repetir)
    table = pa.Table.from_pandas(amenidades_df) 
    pq.write_table(table, f"gs://{bucket_name}/{file_amenities_parquet}")
    print(f"Parquet file successfully uploaded to GCS: {file_amenities_parquet}")
