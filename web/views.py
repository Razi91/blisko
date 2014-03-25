from django.shortcuts import render
from django.http import HttpResponse
from django.template import Context, Template
from django.shortcuts import render_to_response
# Create your views here.


USER = 1
TEACHER = 2

def require(request, right):
    """
        Sprawdza prawa do widoku, podnosi 404 lub 500 w przypadku błędu
    """
    pass

def User(request):
    """
        Zwraca zalogowanego użytkownika lub None
    """
    pass

def get(request):
    """
        Ogólna mapa do użytku w szablonach
    """
    map = {}
    return map






def main(request):
    map = get(request)
    return render_to_response('main.html', map)