from django.shortcuts import render, redirect
from google.cloud import storage
import pyarrow.parquet as pq
import pandas as pd
from django.shortcuts import render
import io


def reviews_view(request):
    try:
        bucket_name = 'hotelwise_db'
        file_name = 'state_city_data.csv'

        # Create GCS client (optional, reuse if already exists)
        #   os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
        #   client = storage.Client.from_service_account_json(GOOGLE_APPLICATION_CREDENTIALS)
        client = storage.Client.from_service_account_json("./key.json")

        blob = client.bucket(bucket_name).blob(file_name)
        data = blob.download_as_string()
        locations_df = pd.read_csv(io.StringIO(data))
        # Unique states for dropdown
        states = list(locations_df['STATE'].unique())
        cities_dict = {}
        for state in states:
            cities_dict[state] = list(
                locations_df[locations_df['STATE'] == state]['CITY'])
        if request.method == 'POST':
            selected_state = request.POST.get('selected_state')
            selected_city = request.POST.get('selected_city')
            if selected_state and selected_city and selected_city in cities_dict.get(selected_state, []):
                print("Something")

    except (IOError, PermissionError, Exception) as e:  # Catch potential errors
        # Handle errors gracefully (e.g., log the exception, display an error message)
        print(f"Error accessing CSV data from GCS: {e}")
        # Redirect to an error page or display error message
        # Assuming you've set up the error_page URL
        return redirect('error_page')

    # ... rest of your view logic using states and cities_dict

    return render(request, 'reviews.html', {'States': states, 'Cities': cities_dict})


def error_page(request):
    return render(request, 'error_page.html')
