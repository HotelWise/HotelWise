from .views import reviews_view, get_cities, ml_html
from django.urls import path


urlpatterns = [
    path('', reviews_view, name='reviews'),
    path('get_cities/', get_cities, name='get_cities'),
    path('ML_HTML/', ml_html, name='ml_html'),
    # path('error_page', views.error_page, name='error_page'),
]
