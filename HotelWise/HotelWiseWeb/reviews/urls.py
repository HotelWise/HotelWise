from .views import reviews_view, get_cities
from django.urls import path
from . import views


urlpatterns = [
    path('', reviews_view, name='reviews'),
    path('get_cities/', get_cities, name='get_cities'),
    # path('error_page', views.error_page, name='error_page'),
]
