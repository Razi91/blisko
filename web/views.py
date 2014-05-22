from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from django.template import Context, Template
from django.shortcuts import render_to_response
from web.models import *
# Create your views here.


USER = 1
TEACHER = 2

def user(request: HttpRequest):
    """
        Zwraca zalogowanego użytkownika lub None
    """
    id = request.session.get('user', 0)
    user = User.objects.get(id=id)
    return user

def get(request: HttpRequest):
    """
        Ogólna mapa do użytku w szablonach
    """
    map = {}
    map['user'] = user(request)
    return map



def login(request: HttpRequest):
    pass

def logout(request: HttpRequest):
    request.session['user'] = None
    pass


def main(request: HttpRequest):
    map = get(request)
    map['courses'] = Courses.objects.all()
    return render_to_response('courses_list.html', map)

def tests(request):
    """
        Lista dostępnych testów
    """
    map = get(request)
    group = user(request).groups()
    #tests = Test.objects.all().filter(course = group.course)
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








