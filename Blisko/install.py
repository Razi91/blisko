# -*- coding: utf-8 -*-
__author__ = 'jkonieczny'
"""
    Plik zawiera skrypty instalujące podstawową konfigurację systemu
"""

from web.models import *
from Blisko import settings
import json
from django.db import transaction


def install_basic():
    """
        Kompletnie podstawowa konfiguracja do wywołania zaraz po zresetowaniu bazy danych
    """
    priv = AccountPrivilages()
    priv.name = "użytkownik"
    priv.level = 1
    priv.save()
    user = User()
    user.id = 0
    user.login = "Niezalogowany"
    user.privilages = priv
    user.email = "nope@nope.com"
    user.save()

    moderator = AccountPrivilages()
    moderator.name = "moderator"
    moderator.level = 4
    moderator.save()

    edytor = AccountPrivilages()
    edytor.name = "edytor"
    edytor.level = 2
    edytor.save()


def install_course(kurs):
    print("Kurs " + kurs)
    dir = settings.BASE_DIR + "/kursy/" + kurs + "/"
    with open(dir + "data.json") as data:
        course = Course()
        data = json.loads(data.read())
        course.name = data['title']
        course.short = data['short']
        course.long = data['long']
        course.cost = data['cost']
        course.level = 1
        course.save()
        for lesson in data['lessons']:
            print("  Lekcja " + lesson['title'])
            les = Lesson()
            les.name = lesson['title']
            with open(dir + "/" + lesson['file']) as content:
                les.content = content.read()
            les.course = course
            les.save()
        for test in data['tests']:
            t = Test()
            print("  Test " + test['file'])
            with open(dir + "/" + test['file']) as ts:
                ts = json.loads(ts.read())
                t.name = ts['title']
                t.points = len(ts['questions'])
                t.course = course
                t.save()
                for question in ts['questions']:
                    quest = Question()
                    quest.type = Question.CLOSED_BINARY
                    quest.test = t
                    quest.content = question['question']
                    quest.save()
                    for ans in question['correct']:
                        a = Answer()
                        a.question = quest
                        a.correct = True
                        a.text = ans
                        a.save()
                    for ans in question['false']:
                        a = Answer()
                        a.question = quest
                        a.correct = False
                        a.text = ans
                        a.save()
                t.course = course
                #course


def install_tests():
    """
    Instalacja kursów
    """
    with transaction.atomic():
        kursy = ["JSON", "Canvas"]
        for kurs in kursy:
            install_course(kurs)
