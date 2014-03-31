from django.shortcuts import render
from django.http import HttpResponse
from django.template import Context, Template
from django.shortcuts import render_to_response
from web import models
from web import views
import json
# Create your views here.

def user_groups(request):
    """
        JSON dla grup do których należy użytkownik
        prawa: użytkownik
    """
    pass

def user_last_results(request):
    """
        JSON dla ostatnich osiągnięć użytkownika
        prawa: użytkownik lub prowadzący
    """
    pass

def user_last_activity(request):
    """
        JSON dla ostatnich aktywności użytkownika
        prawa: prowadzący
    """
    pass

def questions_for_test(request, test):
    """
        JSON dla pytań
        prawa: użytkownik
    """
    id = 0
    tests = models.Test.objects.all().filter(id = test)
    questions = models.Questions.objects.all().filter(test = id)
    js = {}
    js["questions"]=[]
    for question in questions:
        anss = models.Answers.objects.all().filter(question = question)
        answers = []
        for an in anss:
            answers.append(an.id, an.text)
        desc={"text": question.text,
              "image": question.image,
              "answers": answers}
        js["questions"].append(desc)
    return HttpResponse(json.dumps(js), content_type="application/json")