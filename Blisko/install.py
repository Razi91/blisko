# -*- coding: utf-8 -*-
__author__ = 'jkonieczny'
"""
    Plik zawiera skrypty instalujące podstawową konfigurację systemu
"""

from web.models import *
import json

def install_basic():
    """
        Kompletnie podstawowa konfiguracja do wywołania zaraz po zresetowaniu bazy danych
    """
    user = User()
    user.id = 0
    user.login = "Niezalogowany"
    user.privilages_id = 0
    user.save()

def install_tests():
    """
    Instalacja kursów
    """
    kursy = ["JSON"]
    for kurs in kursy:
        dir = BASE_DIR+"/kursy/"+kurs+"/"
        with open(dir+"data.json") as data:
            course = Course()
            data = json.loads(data.read())
            course.name = data['title']
            course.short = data['short']
            course.long = data['long']
            course.save()
            #objs = []
            for lesson in data['lessons']:
                les = Lesson()
                les.name = data['title']
                with open(dir+"/"+lesson['file']) as content:
                    les.content = content.read()
                les.course = course
                #objs.append(les)
                les.save()
            for test in data['tests']:
                t = Test()
                t.points = len(len(ts['questions']))
                with open(dir+"/"+test['file']) as ts:
                    ts = json.loads(ts)
                    t.name = ts['title']
                    for question in ts['questions']:
                        quest = Question()
                        quest.type = Question.CLOSED_BINARY
                        quest.test = t
                        question.content =  question['question']
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
                    t.save()
    pass