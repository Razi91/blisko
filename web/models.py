# -*- coding: utf-8 -*-
from django.db import models
import random
# Create your models here.

class AccountPrivilages(models.Model):
    """
        Definiuje przywileje konta
    """
    name = models.CharField(max_length=40)
    level = models.IntegerField()
    class Meta:
        db_table = "AccountPrivilages"


class User(models.Model):
    """
        Model użytkownika
    """
    login = models.CharField(max_length=30, unique=True)
    password = models.CharField(max_length=128)
    real_name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    privilages = models.ForeignKey(AccountPrivilages)
    enabled = models.BooleanField(default=0)
    credits = models.IntegerField(default=0)

    def is_logged(self):
        return self.id != 0

    def can_buy(self, course):
        return course.cost <= self.credits
    
    def is_doing_test(self):
        """
            Wykonuje obecnie test
            TODO
        """
        return False
    
    def is_watching_lesson(self):
        """
            Ogląda lekcje
            TODO
        """
        return False
    
    def available_tests(self):
        """
            Dostępne testy
        """
        if self.is_doing_test() or self.is_watching_lesson(): return None
        tests = []
        #TODO: pobrać testy
        return tests
        
    def available_lessons(self):
        """
            Dostępne lekcje do obejrzenia
        """
        if self.is_doing_test(): return None
        #TODO
        return []
    
    def set_password(self, raw_password):
        algo = 'sha1'
        salt = get_hexdigest(algo, str(random.random()), str(random.random()))[:5]
        hsh = get_hexdigest(algo, salt, raw_password)
        self.password = '%s$%s$%s' % (algo, salt, hsh)
        
    def check_password(self, raw_password):
        algo = 'sha1'
        salt = get_hexdigest(algo, str(random.random()), str(random.random()))[:5]
        hsh = get_hexdigest(algo, salt, raw_password)
        password = '%s$%s$%s' % (algo, salt, hsh)
        return password == self.password
    
    def _str_(self):
        return person.name
    
    class Meta:
        db_table = "User"

class Course(models.Model):
    name = models.CharField(max_length=40)
    short = models.CharField(max_length=40)
    long = models.TextField()
    level = models.IntegerField()
    cost = models.IntegerField()
    class Meta:
        db_table = "Course"


class Group(models.Model):
    """
        Grupa biorąca udział w kursie
    """
    name = models.CharField(max_length=40)
    teacher = models.ForeignKey(User)
    course = models.ForeignKey(Course)
    # students = models.ManyToManyField(User, through='Students')
    class Meta:
        db_table = "Group"
        
class CourseAccess(models.Model):
    """
        Dostęp użytkownika do kursu
    """
    user = models.ForeignKey(User)
    course = models.ForeignKey(Course)
    date = models.DateField()
    class Meta:
        db_table = "CourseAccess"
    
    
class Lesson(models.Model):
    name = models.CharField(max_length=40)
    content = models.TextField()
    course = models.ForeignKey(Course)
    class Meta:
        db_table = "Lesson"
    
    
class Test(models.Model):
    name = models.CharField(max_length=40)
    points = models.IntegerField()
    #attempts = models.IntegerField()
    course = models.ForeignKey(Course)
    
    fromJson = False
    parsedQuestions = []
    
    def questions(self):
        return Question.objects.filter(test=self)
    
    def parse(self, json):
        """
            Generuje strukturę z odpowiedziami z JSona
        """
        fromJson = True
        pass
    
    def points(self):
        """
            Punkty zdobyte
        """
        #if not fromJson: return
        pts = 0
        for question in parsedQuestions:
            pts += question.pts
        return pts
    
    def done_by_user(self, user):
        """
            Test wykonany już przez użytkownika
        """
        if Result.objects.filter(user=user).count() > 0: 
            return True
        return False
    
    def is_available_for_user(self, user):
        """
        """
        pass
    
    class Meta:
        db_table = "Test"
        
        
class TestAvailability(models.Model):
    start = models.DateTimeField()
    end = models.DateTimeField()


class Question(models.Model):
    OPEN = "o"
    CLOSED_ONE = "c"
    CLOSED_MANY = "m"
    CLOSED_BINARY = "b"
    TYPE = (
          (OPEN, "Otwarte"),
          (CLOSED_ONE, "Zamknięte"),
          (CLOSED_MANY, "Zamknięte w."),
          (CLOSED_BINARY, "Zamknięte b."))
    test = models.ForeignKey(Test)
    content = models.TextField()
    type = models.CharField(max_length=1, choices=TYPE, default=CLOSED_ONE)
    points = models.IntegerField()

    def answers(self):
        return Answer.objects.filter(question=self)

    class Meta:
        db_table = "Question"
    
    def no_error(self):
        if type == Question.OPEN:
            return True
        list = Answer.objects.get(question=self)
        correct = 0
        for ans in list:
            if ans.correct: correct += 1
        if type == Question.CLOSED_ONE and correct == 1:
            return True
        elif type == Question.CLOSED_MANT and correct > 0:
            return True
        return False
    
    def points(self, anss):
        """
        Punkty zdobyte w tym zadaniu
        """
        list = Answer.objects.get(question=self)
        v = 0
        for ans in list:
            if ans.is_correct() and ans.id in anss:
                v += 1
        return v
    
    class Meta:
        db_table = "Question"
        
        
class Answer(models.Model):
    question = models.ForeignKey(Question)
    text = models.TextField()
    #image = models.TextField()
    correct = models.BooleanField()
    
    def is_correct(self, ans):
        return ans == correct
    
    class Meta:
        db_table = "Answer"
        
class OpenAnswer(models.Model):
    user = models.ForeignKey(User)
    question = models.ForeignKey(Question)
    sesid = models.IntegerField()
    points = models.IntegerField(default = -1)
    
    class Meta:
        db_table = "OpenAnswer"
    
    
class Result(models.Model):
    date = models.DateTimeField(auto_now=True)
    startdate = models.DateTimeField(auto_now=True)
    percent = models.FloatField()
    user = models.ForeignKey(User)
    test = models.ForeignKey(Test)
    
    class Meta:
        db_table = "Result"
    
    
class Activity(models.Model):
    UNKNOWN = "un"
    OPEN_TEST = "ot"
    OPEN_LESSON = "ol"
    CLOSE_TEST = "ct"
    CLOSE_LESSON = "cl"
    ACTIVITY_TYPE = (
                   (UNKNOWN, "nieznana"),
                   (OPEN_TEST, "Otwarcie testu"),
                   (CLOSE_TEST, "Zamknięcie testu"),
                   (OPEN_LESSON, "Otwarcie lekcji"),
                   (CLOSE_LESSON, "Zamknięcie lekcji"))
    user = models.ForeignKey(User)
    date = models.DateTimeField(auto_now=True)
    activityid = models.IntegerField()
    ipv4 = models.IntegerField()
    type = models.CharField(max_length=2, choices=ACTIVITY_TYPE, default=UNKNOWN)
    
    class Meta:
        db_table = "Activity"
    
"""
Notatki jkonieczny

    SELECTy dla testu + pytania + odpowiedzi

    SELECT * FROM Question WHERE test = id_testu
    
    SELECT * FROM Answer WHERE question = id_question


"""


