# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from django.core.context_processors import csrf
from django.db import models
from django.template import Context, Template
#from settings import *
from django.shortcuts import render_to_response
from web.messages import *
from web.models import *
from web import utils
from web import messages
from web import tester
import re
import datetime

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
    platform = {
        "courses": Course.objects.all().count(),
        "lessons": Lesson.objects.all().count(),
        "tests": Test.objects.all().count(),
        "users": User.objects.all().count()
    }
    map['owned_courses'] = CourseAccess.objects.all().filter(user=map['user'])
    map['platform'] = platform
    return map


def login(request: HttpRequest):
    if request.method == 'POST':
        login = request.POST.get('login', "")
        password = request.POST.get('pass', "")
        try:
            user = User.objects.get(login=login)
            print(password)
            print(utils.hash_password(password))
            print(user.password)
            if not utils.check_password(user.password, password):
                map = get(request)
                msg = messages.Message("Błąd logowania", "Złe hasło", [])
                map['msg'] = msg
                return render_to_response('main.html', map)
            request.session['user'] = user.id
            map = get(request)
            msg = messages.Message("Zalogowano", "Logowanie przebiegło pomyślnie", [])
            map['msg'] = msg
            return render_to_response('main.html', map)
        except User.DoesNotExist:
            map = get(request)
            msg = messages.Message("Błąd logowania", "Użytkownik nie istnieje", [])
            map['msg'] = msg
            return render_to_response('main.html', map)
    map = get(request)
    return render_to_response('main.html', map)


def logout(request: HttpRequest):
    request.session['user'] = 0
    map = get(request)
    msg = messages.Message("Wylogowano!", "Zostałeś wylogowany z serwisu", [])
    map['msg'] = msg
    return render_to_response('main.html', map)


def doladuj(request: HttpRequest):
    request.session['user'] = 0
    map = get(request)
    return render_to_response('doladuj.html', map)


def register(request: HttpRequest):
    if request.method == 'POST':
        login = request.POST.get('login', "")
        password1 = request.POST.get('pass1', -1)
        password2 = request.POST.get('pass2', -1)
        realname = request.POST.get('realname', "")
        email = request.POST.get('email', "")
        map = get(request)
        map['login'] = login
        map['email'] = email
        map['realname'] = realname
        if password1 != password2:
            msg = messages.Message("Hasła nie zgadzają się!", [])
            map['msg'] = msg
        elif len(password1) < 4:
            msg = messages.Message("Twoje hasło jest za krótkie!", [])
            map['msg'] = msg
        elif not re.match(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$", email):
            msg = messages.Message("Wprowadź poprawnie adres email", [])
            map['msg'] = msg
        else:
            msg = messages.Message("Błąd!", "Rejestracja nie powiodła się, sprawdź wprowadzone dane.", [])
            map = get(request)
            map['msg'] = msg
            map['login'] = login
            map['email'] = email
            map['realname'] = realname
            user = User()
            user.login = login
            user.email = email
            user.real_name = realname
            print(password1)
            user.password = utils.hash_password(password1)
            print(user.password)
            user.privilages = AccountPrivilages.objects.get(id=1)
            user.credits = 100
            user.save()
            map = get(request)
            return render_to_response('main.html', map)
    else:
        map = get(request)
    return render_to_response('register.html', map)


def main(request: HttpRequest):
    map = get(request)
    return render_to_response('main.html', map)


def kursy(request: HttpRequest):
    map = get(request)
    map['courses'] = Course.objects.all()
    user = map['user']
    map['styles'] = ["courses"]
    for course in map['courses']:
        course.for_user(user)
    return render_to_response('courses_list.html', map)


def cert(request: HttpRequest, id):
    id = int(id)
    map = get(request)
    try:
        course = Course.objects.get(id=id)
        course.for_user(map['user'])
        if course.finished():
            map['course'] = course
            return render_to_response('cert.html', map)
        else:
            raise "brak praw"
    except:
        return render_to_response('main.html', map)


def kurs(request: HttpRequest, id):
    id = int(id)
    map = get(request)
    try:
        course = Course.objects.get(id=id)
        course.for_user(map['user'])
        #if not course.is_owned():
        #    return login(request)
        if request.method == 'POST':
            content = request.POST.get("content", "")
            if len(content) > 3:
                com = Comment()
                com.user = map['user']
                com.course = course
                com.date = datetime.datetime.now()
                com.visibility = True
                com.content = content
                com.save()
        map['course'] = course
        course.for_user(map['user'], True)
        comments = Comment.objects.filter(course=course)
        map['comments'] = comments
        return render_to_response('course.html', map)
    except Course.DoesNotExist:
        return render_to_response('main.html', map)


def kursWyslij(request: HttpRequest, id):
    id = int(id)
    map = get(request)
    try:
        course = Course.objects.get(id=id)
        map['course'] = course
        user = map['user']
        course.for_user(map['user'], True)
        if not course.is_owned():
            return login(request)
        testid = request.POST.get("test", -1)
        if testid == -1:
            raise Course.DoesNotExist
        test = Test.objects.get(id=testid)
        pts, max = tester.points(request.POST, test)
        try:
            old = Result.objects.get(user=user, test=test)
            byl = True
            old_procent = old.percent
            old.delete()
        except:
            old_procent = -1
            pass
        procent = 100.0 * pts / max
        if old_procent < procent:
            result = Result()
            result.user = user
            result.test = test
            result.date = datetime.datetime.now()
            result.startdate = datetime.datetime.now()
            result.percent = procent
            result.save()
            action = ActionUrl("/kurs/%d/" % course.id, "Wróć do kursu")
            #msg=Message("Wysłano test", "Twój wynik to "+str(result.percent) + "%", [action])
            #map['msg'] = msg
            access = CourseAccess.objects.get(user=user, course=course)
            if not access.completed:
                tests = course.tests()
                try:
                    for test in tests:
                        res = Result.objects.get(user=user, test=test)
                        if res.percent != 100:
                            print("nie 100%")
                            raise "not 100%"
                    access.completed = True
                    access.save()
                    user.credits += course.cost / 10
                    user.save()
                except:
                    import sys
                    print(sys.exc_info()[0])
                    pass
            course.for_user(map['user'], True)
        return render_to_response('course.html', map)
    except Course.DoesNotExist:
        return render_to_response('main.html', map)


def kup(request: HttpRequest, id):
    id = int(id)
    map = get(request)
    user = map['user']
    try:
        course = Course.objects.get(id=id)
        if CourseAccess.objects.filter(user=user, course=course).count() > 0:
            return main(request)
        user.credits -= course.cost
        acc = CourseAccess()
        acc.user = user
        acc.course = course
        acc.date = datetime.datetime.now()
        acc.save()
        user.save()
        action = ActionUrl("/kurs/%d/" % course.id, "Idź do kursu")
        msg = messages.Message("Kurs zakupiony!", "Możesz teraz przeglądać lekcje i wykonywać testy",
                               [action, ActionBack()])
        map['msg'] = msg
        return render_to_response('boxonly.html', map)
    except Course.DoesNotExist:
        map = get(request)
        msg = messages.Message("Błąd", "Kurs nie istnieje", [ActionBack()])
        map['msg'] = msg
        return render_to_response('courses_list.html', map)
    return render_to_response('courses_list.html', map)


def lekcja(request: HttpRequest, id):
    id = int(id)
    try:
        map = get(request)
        lesson = Lesson.objects.get(id=id)
        lesson.course.for_user(map['user'])
        if not lesson.course.is_owned():
            return login(request)
        map['lesson'] = lesson
        return render_to_response('lesson.html', map)
    except Lesson.DoesNotExist:
        map = get(request)
        return render_to_response('main.html', map)


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
    map = get(request)
    test = Test.objects.all().filter(id=id)[0]
    test.course.for_user(map['user'])
    if not test.course.is_owned():
        return login(request)
    map['styles'] = ["test"]
    #test.is_available_for_user(user)
    map['test'] = test
    return render_to_response('test.html', map)


def o_platformie(request: HttpRequest):
    map = get(request)
    return render_to_response('about.html', map)


#error







