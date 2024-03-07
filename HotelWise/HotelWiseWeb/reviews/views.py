# reviews/views.py
from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse
from .models import State, City
import requests
import json


def reviews_view(request):
    states = State.objects.all()
    cities = []

    selected_state_name = request.GET.get('state')
    if selected_state_name:
        selected_state = State.objects.get(name=selected_state_name)
        cities = City.objects.filter(state=selected_state)

    return render(request, 'reviews.html', {'states': states, 'cities': cities})


def get_cities(request):
    selected_state_name = request.GET.get('state')
    if selected_state_name:
        selected_state = State.objects.get(name=selected_state_name)
        cities = City.objects.filter(state=selected_state)
        city_names = [city.name for city in cities]
        return JsonResponse(city_names, safe=False)
    else:
        return JsonResponse([], safe=False)


def save_location(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        selected_state = data.get('state')
        selected_city = data.get('city')
        response_data = send_data(selected_state, selected_city)
        print(response_data)
        print(type(response_data))
        return JsonResponse(response_data)
    else:
        return ('error Invalid request method')


def send_data(selected_state, selected_city):
    cloud_function_url = "https://us-central1-hotelwiseweb.cloudfunctions.net/ML_HTML"
    payload = {
        "state": selected_state,
        "city": selected_city
    }
    headers = {
        "Content-Type": "application/json"
    }
    response = requests.post(cloud_function_url, json=payload, headers=headers)
    print("Status Code:", response.status_code)
    if response.status_code == 200:
        print("Cloud function successfully triggered.")
        try:
            response_json = response.json()
            print("Response Content:", response_json)
            return (response_json)
        except ValueError:
            print("Response Content (raw):", response.content.decode('utf-8'))
    else:
        print("Error triggering cloud function. Status code:", response.status_code)
        print("Error Response Content:", response.content.decode('utf-8'))
