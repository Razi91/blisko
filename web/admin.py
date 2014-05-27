from django.contrib import admin
from web.models import *

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    pass
admin.site.register(User, UserAdmin)

class CourseAdmin(admin.ModelAdmin):
    pass
admin.site.register(Course, CourseAdmin)

class CourseAccessAdmin(admin.ModelAdmin):
    pass
admin.site.register(CourseAccess, CourseAccessAdmin)

class LessonAdmin(admin.ModelAdmin):
    pass
admin.site.register(Lesson, LessonAdmin)

class QuestionAdmin(admin.ModelAdmin):
    pass
admin.site.register(Question, QuestionAdmin)

class AnswerAdmin(admin.ModelAdmin):
    pass
admin.site.register(Answer, AnswerAdmin)

class OpenAnswerAdmin(admin.ModelAdmin):
    pass
admin.site.register(OpenAnswer, OpenAnswerAdmin)

class ResultAdmin(admin.ModelAdmin):
    pass
admin.site.register(Result, ResultAdmin)

class ActivityAdmin(admin.ModelAdmin):
    pass
admin.site.register(Activity, ActivityAdmin)

class CommentAdmin(admin.ModelAdmin):
    pass
admin.site.register(Comment, CommentAdmin)
