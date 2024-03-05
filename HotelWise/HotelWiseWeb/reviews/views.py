# reviews/views.py
from django.shortcuts import render
from django.http import JsonResponse
from .models import State, City
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


def get_google_cloud_identity_token(request):
    with open('path/to/your/key.json', 'r') as file:
        key_data = json.load(file)
        token = key_data.get('private_key', None)
    return render(request, 'reviews.html', {'token': token})


def ml_html(request):
    if request.method == 'POST':
        # Your Cloud Function logic here
        data = request.POST
        state = data.get('state')
        city = data.get('city')

        # Process the request and return a response
        response_data = {
            'message': 'Request received successfully',
            'state': state,
            'city': city
        }
        return JsonResponse(response_data)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
