import functions_framework
from DB_FIX_Amenities import process_amenities
from DB_FIX_Crime import process_crime
from DB_NLP_NLTK import process_nlp
from DB_Extract_Amenities import *
from DB_Extract_Location import *

@functions_framework.cloud_event
def process_hotel_data(cloud_event):
    data = cloud_event.data

    event_id = cloud_event["id"]
    event_type = cloud_event["type"]

    bucket = data["bucket"]
    name = data["name"]
    metageneration = data["metageneration"]
    timeCreated = data["timeCreated"]
    updated = data["updated"]

    print(f"Event ID: {event_id}")
    print(f"Event type: {event_type}")
    print(f"Bucket: {bucket}")
    print(f"File: {name}")
    print(f"Metageneration: {metageneration}")
    print(f"Created: {timeCreated}")
    print(f"Updated: {updated}")

    print("Comienza FIX Amenities")
    process_amenities()
    print("Comienza FIX Crime")
    process_crime()
    print("Comienza NLP")
    process_nlp()
    print("Comienza Extract Amenities")
    extract_amenities()
    print("Comienza Extract Location")
    extract_location()
    print("Se termino el proceso de trabajo completo")