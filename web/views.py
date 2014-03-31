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

def user(request):
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

def tests(request):
    """
        Lista dostępnych testów
    """
    map = get(request)
    group = user(request).groups()
    tests = Test.objects.all().filter(course = group.course)
    return render_to_response('main.html', map)


def test(request, id):
    """
        Szczegóły testu
    """
    map = get(request)
    group = user(request).groups()
    test = Test.objects.all().filter(id = id)[0]
    test.is_available_for_user(user)
    return render_to_response('main.html', map)








