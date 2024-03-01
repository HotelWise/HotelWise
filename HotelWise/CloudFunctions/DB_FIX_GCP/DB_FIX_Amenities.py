from google.cloud import storage
import pandas as pd
import random


def process_amenities():
    project_id = "hotelwiseweb"
    bucket_name1 = "hotelwise_bucket"
    bucket_name2 = "hotelwise_db"
    file_name_excel = "hoteles_unificado.xlsx"
    file_name_parquet = "HotelesUnificado.parquet"

    client = storage.Client(project=project_id)
    bucket = client.bucket(bucket_name1)

    hoteles_dataset = pd.read_excel(f"gs://{bucket_name1}/{file_name_excel}")

    hoteles_dataset.columns = hoteles_dataset.columns.str.upper()

    # Lista de 30 amenidades
    amenities_list = [
        'Pool', 'Gym', 'Restaurant', 'Bar', 'Spa',
        'Free Wi-Fi', 'Complimentary Breakfast', 'Room Service', 'Free Parking', '24-Hour Reception',
        'Business Center', 'Conference Room', 'Laundry Service', 'Daily Housekeeping', 'Air Conditioning',
        'Heating', 'Jacuzzi', 'Sauna', 'Hot Tub', 'Airport Shuttle Service',
        'Concierge Service', 'Accessible Accommodations', 'Family Rooms', 'Terrace or Garden',
        'Bicycle Rental Service', 'Beauty Salon', 'Luggage Storage', 'Children\'s Play Area',
        'Multilingual Staff', 'Soundproof Rooms'
    ]

    # Lista extendida + 30 amenidades
    amenities_list.extend([
        'Free Fitness Classes', 'Pet-Friendly', 'Indoor Pool', 'Outdoor Pool', 'Tennis Courts',
        'Basketball Court', 'Volleyball Court', 'Yoga Classes', 'Fitness Center', 'Library',
        'Game Room', 'Billiards', 'Ping Pong Table', 'Movie Theater', 'Karaoke Room',
        'Live Entertainment', 'Gift Shop', 'Mini Market', 'ATM', 'Currency Exchange',
        'Car Rental', 'Airport Shuttle', 'Train Station Shuttle', 'Beach Access', 'Water Sports',
        'Golf Course', 'Ski Resort Shuttle', 'Ski Equipment Rental', 'Hiking Trails', 'Bike Trails'
    ])
    # Definir función para seleccionar 5 amenidades al azar sin repetición

    def select_random_amenities():
        return random.sample(amenities_list, k=5)

    # Llenar la columna 'amenities' con 5 amenidades aleatorias
    hoteles_dataset['AMENITIES'] = hoteles_dataset.apply(
        lambda x: select_random_amenities(), axis=1)

    hoteles_para_guardar = hoteles_dataset[[
        'NAME', 'LATITUDE', 'LONGITUDE', 'CITY',
        'COUNTY', 'STATE', 'TEXT',
        'AVG_RATING', 'AMENITIES']]

    print(hoteles_para_guardar.head())

    hoteles_para_guardar.to_parquet(
        f"gs://{bucket_name2}/{file_name_parquet}", index=False)

    print(f"Parquet file successfully uploaded to GCS: {file_name_parquet}")
