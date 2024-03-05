from django.urls import path
from . import views

urlpatterns = [
    path('', views.reviews_view, name='reviews'),
    # path('error_page', views.error_page, name='error_page'),
]
