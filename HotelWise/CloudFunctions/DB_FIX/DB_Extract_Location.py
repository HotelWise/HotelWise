import pyarrow as pa 
import pyarrow.parquet as pq
import pandas as pd
from DB_FILES import *

def extract_location():
    hoteles_dataset_NLP = pd.read_parquet(f"gs://{bucket_name}/{file_hoteles_NLP_parquet}")
    state_city_dict = {}
    for row in hoteles_dataset_NLP.itertuples():
        state = row.STATE
        city = row.CITY
        if state not in state_city_dict:
            state_city_dict[state] = []
        if city not in state_city_dict[state]:
            state_city_dict[state].append(city)
    city_lists = []
    for state, city_list in state_city_dict.items():
        city_lists.append({'STATE': state, 'CITY': city_list})
    state_city_df = pd.DataFrame(city_lists)
    table = pa.Table.from_pandas(state_city_df) 
    pq.write_table(table, f"gs://{bucket_name}/{file_locations_parquet}")
    print(f"Parquet file successfully uploaded to GCS: {file_locations_parquet}")
