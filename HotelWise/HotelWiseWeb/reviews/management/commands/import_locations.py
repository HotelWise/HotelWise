# reviews/management/command/import_locations.py
from django.core.management.base import BaseCommand
from reviews.models import State, City
import pandas as pd
import ast
from google.cloud import storage
import io


class Command(BaseCommand):
    help = 'Imports locations from CSV'

    def handle(self, *args, **kwargs):
        client = storage.Client.from_service_account_json(
            "../HotelWiseWeb/key.json")
        storage_client = storage.Client()
        # Specify your bucket name and file name
        bucket_name = 'hotelwise_db'
        file_name = 'state_city_data.csv'

        # Get the bucket and blob
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(file_name)

        # Download the file as bytes
        data = blob.download_as_string()

        # Convert bytes to a pandas DataFrame
        locations_df = pd.read_csv(io.BytesIO(data))

        # Process the DataFrame and populate the database
        for index, row in locations_df.iterrows():
            state, cities = row['STATE'], ast.literal_eval(row['CITY'])
            state_obj, _ = State.objects.get_or_create(name=state)
            cities.sort()
            for city in cities:
                if city:
                    City.objects.get_or_create(state=state_obj, name=city)
