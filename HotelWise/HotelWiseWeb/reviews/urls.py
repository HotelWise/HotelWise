from .views import reviews_view, get_cities, save_location, send_data
from django.urls import path


urlpatterns = [
    path('', reviews_view, name='reviews'),
    path('get_cities/', get_cities, name='get_cities'),
    path('save_location/', save_location, name='save_location'),
    path('send_data/', send_data, name='send_data'),
]
