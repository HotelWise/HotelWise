# reviews/views.py
from django.shortcuts import render
from .models import State, City


def reviews_view(request):
    states = State.objects.all()
    cities = []

    selected_state = request.GET.get('state')
    if selected_state:
        cities = City.objects.filter(state__name=selected_state)

    return render(request, 'reviews.html', {'states': states, 'cities': cities})
