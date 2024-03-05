# reviews/views.py
from django.shortcuts import render
from django.http import JsonResponse
from .models import State, City


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
