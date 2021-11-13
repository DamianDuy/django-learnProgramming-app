from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Programming_Language)
@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display=[ 'name', 'programming_lang', 'author' ]

@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display= [ 'name', 'related_lang', 'subject', 'author' ]

    def related_lang(self, obj):
        return obj.subject.programming_lang.name
    related_lang.short_description = 'Language'

admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(User_Answer)
admin.site.register(Answers_Data)
admin.site.register(Subject_Point)
admin.site.register(Test_Point)
admin.site.register(Question_Point)
admin.site.register(Rating)
