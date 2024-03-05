from django.shortcuts import render, redirect
from google.cloud import storage
import pyarrow.parquet as pq
import pandas as pd
from django.shortcuts import render
import io


def reviews_view(request):
    bucket_name = 'hotelwise_db'
    file_name = 'state_city_data.csv'

    # Create GCS client (optional, reuse if already exists)
    #   os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
    #   client = storage.Client.from_service_account_json(GOOGLE_APPLICATION_CREDENTIALS)
    client = storage.Client.from_service_account_json("./key.json")

    blob = client.bucket(bucket_name).blob(file_name)
    data = blob.download_as_bytes()  # Download as bytes
    data = io.BytesIO(data)  # Create a BytesIO object
    locations_df = pd.read_csv(data)
    states = list(locations_df['STATE'].unique())
    cities_dict = {}
    print(states)
    for state in states:
        cities_dict[state] = list(
            locations_df[locations_df['STATE'] == state]['CITY'])
    if request.method == 'POST':
        selected_state = request.POST.get('selected_state')
        selected_city = request.POST.get('selected_city')
        if selected_state and selected_city and selected_city in cities_dict.get(selected_state, []):
            print("Something")

    return render(request, 'reviews.html', {'States': states, 'Cities': cities_dict})


def error_page(request):
    return render(request, 'error_page.html')
