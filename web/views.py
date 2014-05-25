# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from django.core.context_processors import csrf
from django.template import Context, Template
#from settings import *
from django.shortcuts import render_to_response
from web.messages import ActionBack
from web.models import *
from web import utils
from web import messages

import uuid
from django.db import IntegrityError, transaction
from django.contrib.auth.hashers import PBKDF2PasswordHasher
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
    map.update(csrf(request))
    map['user'] = user(request)
    return map


def login(request: HttpRequest):
    if request.method == 'POST':
        map = get(request)
        login = request.post.get('login', "")
        password = request.post.get('pass', "")
        password = utils.hash_password(password)
        user = User.objects.get(login=login)
        if user == None:
            map = get(request)
            #TODO: szablon błędu logowania
            return render_to_response('login_failed.html', map)
        if utils.check_password(hashed_password=user.password, user_password=password):
            map = get(request)
            #TODO: szablon błędu logowania
            return render_to_response('login_failed.html', map)
        #sukces logowania
        request.session['id'] = user.id
        msg = messages.Message("Zalogowano", "Logowanie przebiegło pomyślnie", [ActionBack])
        map['msg'] = msg
        #return render_to_response('msgbox.html', map)
    map = get(request)
    return render_to_response('main.html', map)


def logout(request: HttpRequest):
    request.session['user'] = None
    pass

def register(request: HttpRequest):
    if request.method == 'POST':
        login = request.POST.get('login', -1)
        password1 = request.POST.get('pass1', -1)
        password2 = request.POST.get('pass2', -1)
        email = request.POST.get('email', -1)
        if password1 == password2:
            user = User()
            user.login = login
            user.email=email
            user.password = utils.hash_password(password1)
            user.privilages = AccountPrivilages.objects.get(id=1)
            user.save()
            map = get(request)
            return render_to_response('main.html', map)
        elif len(password1) < 5:
            msg = messages.Message("Twoje hasło jest za krótkie!", [])
            map['msg'] = msg
        else:
            msg = messages.Message("Błąd!", "Rejestracja nie powiodła się, sprawdź wprowadzone dane.", [])
            map = get(request)
            map['msg'] = msg
            map['login'] = login
            map['email'] = email
            return render_to_response('register.html', map)
        pass
    map = get(request)
    return render_to_response('register.html', map)


def main(request: HttpRequest):
    map = get(request)
    return render_to_response('main.html', map)


def kursy(request: HttpRequest):
    map = get(request)
    map['courses'] = Course.objects.all()
    return render_to_response('courses_list.html', map)


def kurs(request: HttpRequest):
    map = get(request)
    return render_to_response('course.html', map)


def lekcja(request: HttpRequest):
    map = get(request)
    return render_to_response('lessons.html', map)


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
        Wykonanie testu
    """
    #TODO: sprawdzić, czy użytkownik ma prawo do tego testu
    #TODO: sprawdzić, czy użytkownik nie ogląda jakiejś lekcji
    map = get(request)
    test = Test.objects.all().filter(id=id)[0]
    map['styles'] = ["test"]
    #test.is_available_for_user(user)
    map['test'] = test
    return render_to_response('test.html', map)

#error







