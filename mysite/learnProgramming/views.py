from django.shortcuts import get_object_or_404, render
from .models import *

# Create your views here.

def about_view(request):
    
    return render( 
        request, 
        'learnProgramming/about.html'
    )

def programming_language_list_view(request):
    programming_language_list = Programming_Language.objects.all()

    context = {
        'programming_language_list': programming_language_list
    }
    
    return render( 
        request, 
        'learnProgramming/index.html', 
        context
    )

def subjects_list_view(request, programming_lang_slug):
    programming_lang = get_object_or_404(Programming_Language, slug=programming_lang_slug)
    subjects_list = Subject.objects.filter(programming_lang=programming_lang)

    context = {
        'programming_lang' : programming_lang,
        'subjects_list' : subjects_list,
    }

    return render(
        request,
        'learnProgramming/subjects_list.html',
        context
    )

def tests_list_view(request, subject_slug):
    subject = get_object_or_404(Subject, slug=subject_slug)
    tests_list = Test.objects.filter(subject=subject)

    context = {
        'programming_lang' : subject.programming_lang,
        'subject' : subject,
        'tests_list' : tests_list,
    }

    return render(
        request,
        'learnProgramming/tests_list.html',
        context
    )

