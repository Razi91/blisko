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
    login = models.CharField(max_length=30)
    password = models.CharField(max_length=128)
    privilages = models.ForeignKey(AccountPrivilages)
    enabled = models.BooleanField()
    
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
    
    
class Group(models.Model):
    """
    Klasa biorąca udział w kursie
    """
    name = models.CharField(max_length=40)
    teacher = models.ForeignKey(User)
    # students = models.ManyToManyField(User, through='Students')
    class Meta:
        db_table = "Group"
    
    
class Students(models.Model):
    user = models.ForeignKey(User)
    group = models.ForeignKey(Group)
    joined = models.DateTimeField()
    class Meta:
        db_table = "Students"
    
    
class Course(models.Model):
    name = models.CharField(max_length=40)
    level = models.IntegerField()
    class Meta:
        db_table = "Course"
    
    
class Lesson(models.Model):
    name = models.CharField(max_length=40)
    content = models.BinaryField()
    course = models.ForeignKey(Course)
    class Meta:
        db_table = "Lesson"
    
    
class Test(models.Model):
    name = models.CharField(max_length=40)
    points = models.IntegerField()
    attempts = models.IntegerField()
    course = models.ForeignKey(Course)
    def done_by_user(self, user):
        if Result.objects.filter(user=user).count() > 0: 
            return True
        return False
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
    class Meta:
        db_table = "Question"
    
    def no_error(self):
        if type == OPEN:
            return True
        list = Answer.objects.get(question=self)
        correct = 0
        for ans in list:
            if ans.correct: correct += 1
        if type == CLOSED_ONE and correct == 1:
            return True
        elif type == CLOSED_MANT and correct > 0:
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
    image = models.TextField()
    correct = models.BooleanField()
    def is_correct(self, ans):
        return ans == correct
    class Meta:
        db_table = "Answer"
    
    
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
    type = models.CharField(max_length=2, choices=ACTIVITY_TYPE, default=UNKNOWN)
    class Meta:
        db_table = "Activity"
    

