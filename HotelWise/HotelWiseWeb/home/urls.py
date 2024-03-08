from django.urls import path
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('acerca_de', views.acerca_de, name='acerca_de'),
    path('contacto', views.contacto, name='contacto'),
    path('error_page', views.error_page, name='error_page'),
    path('dashboard', RedirectView.as_view(
        url='https://lookerstudio.google.com/s/sfapHivroXI'), name='dashboard'),
    path('github', RedirectView.as_view(
        url='https://github.com/HotelWise/HotelWise'), name='github'),
    path('etl', RedirectView.as_view(
        url='https://github.com/HotelWise/HotelWise/tree/ELT-Google'), name='etl'),
    path('d_analytics', RedirectView.as_view(
        url='https://github.com/HotelWise/HotelWise/tree/HotelWise_DA'), name='d_analytics'),
    path('m_learning', RedirectView.as_view(
        url='https://github.com/HotelWise/HotelWise/tree/HotelWiseML'), name='m_learning'),
    path('web_design', RedirectView.as_view(
        url='https://github.com/HotelWise/HotelWise/tree/HotelWiseWeb'), name='web_design'),
    path('seguridad', RedirectView.as_view(
        url='https://github.com/HotelWise/HotelWise/tree/HotelWiseML/HotelWise/Crime_In_The_USA'), name='seguridad'),
]
