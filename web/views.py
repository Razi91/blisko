from django.shortcuts import render
from django.http import HttpResponse
from django.template import Context, Template
from django.shortcuts import render_to_response
# Create your views here.

def get(request):
    map = {}
    map['test'] = "test"
    map['user'] = User()
    
    return map


def main(request):
    map = get(request)
    return render_to_response('main.html', map)