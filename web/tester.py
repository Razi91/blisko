__author__ = 'jkonieczny'
from web.models import *


def points(post, test:Test):
    def getAnss(post):
        anses=[]
        for p in post:
            if p.startswith("ans"):
                anses.append(int(p[3:]))
        return anses
    ##
    anses = getAnss(post)
    pts = 0
    max = 0
    for q in test.questions():
        c = True
        max += 1
        for an in q.answers():
            if (not an.correct) and an.id in anses:
                c = False
                break
            elif an.correct and an.id not in anses:
                c = False
                break
        if c:
            pts+=1
    return pts, max