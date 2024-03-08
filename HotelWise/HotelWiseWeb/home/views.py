from django.shortcuts import render


def home_view(request):
    return render(request, 'home.html')


def acerca_de(request):
    return render(request, 'acerca_de.html')


def contacto(request):
    return render(request, 'contacto.html')


def error_page(request):
    return render(request, 'error_page.html')
