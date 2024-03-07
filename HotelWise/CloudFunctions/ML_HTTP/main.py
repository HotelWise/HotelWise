import functions_framework
from sklearn.metrics.pairwise import cosine_similarity
from google.cloud import storage
import json
import pandas as pd

@functions_framework.http
def recomendacion_hotel(request):
  project_id = "hotelwiseweb"
  bucket_name = "hotelwise_db"
  file_name_parquet = 'Hoteles_NLP_NLTK.parquet'

  client = storage.Client(project=project_id)
  bucket = client.bucket(bucket_name)

  user_reviews_dataset = pd.read_parquet(
  f"gs://{bucket_name}/{file_name_parquet}")

  request_json = request.get_json(silent=True)
  request_args = request.args
  print("Imprimo datos Recibidos:")

  print(f"Request Args: {request_args}")
  print(f"Request json: {request_json}")

  city = request_json['city']
  state = request_json['state']
  
  print("Imprimo datos para trabajar:")
  print(f"City: {city}")
  print(f"State: {state}")
  state_filter = user_reviews_dataset['STATE'] == state
  city_filter = user_reviews_dataset['CITY'] == city
  city_state_filter = user_reviews_dataset[state_filter & city_filter]

  print("Comienzo ML")
  user_reviews_city = user_reviews_dataset[state_filter & city_filter]
  hotel_item_matrix = user_reviews_city.pivot_table(index='CITY', columns=[
                                                    'NAME', 'AVG_RATING', 'CRIME_RATE'], values='SENTIMENT_ANALYSIS', aggfunc='mean', fill_value=0)
  city_row = hotel_item_matrix.loc[city].values.reshape(1, -1)
  similarity_scores = cosine_similarity(city_row, hotel_item_matrix.values)
  similar_users_indices = similarity_scores.argsort()[0][-6:-1]
  recommended_items = hotel_item_matrix.iloc[similar_users_indices].sum(
  ).sort_values(ascending=False).index.tolist()[:3]
  hotel_names_dict = {f"Hotel recomendado {i+1}": name[:31] for i, (name, _, _) in enumerate(recommended_items)}
  hotel_names_json = json.dumps(hotel_names_dict)
  print(hotel_names_json)
  print("Fin ML")
  return(hotel_names_json)