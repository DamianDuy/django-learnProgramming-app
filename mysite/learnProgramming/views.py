from django.shortcuts import get_object_or_404, render, redirect

from .models import *
from .forms import Programming_Language_Form, Subject_Form, Test_Form

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

def add_new_programming_language_view(request):
    if request.method == 'POST':
        form = Programming_Language_Form(request.POST)
        if form.is_valid():
            programming_langugage = form.save()
            return redirect('/programming_language/' + programming_langugage.slug)
    else:
        form = Programming_Language_Form()

    return render(
        request, 
        'learnProgramming/add_new_programming_language.html', 
        {
            'form': form
        }
    )

def add_new_subject_view(request, programming_lang_slug):
    if request.method == 'POST':
        form = Subject_Form(request.POST)
        if form.is_valid():
            #TODO do not create subject from form, get values from form and create Subject object.
            subject = form.save()
            subject.refresh_from_db()
            programming_lang = get_object_or_404(Programming_Language, slug=programming_lang_slug)
            subject.programming_lang = programming_lang
            subject.save()
            return redirect('/subject/' + subject.slug)
    else:
        form = Subject_Form()

    return render(
        request, 
        'learnProgramming/add_new_subject.html', 
        {
            'form': form
        }
    )

def add_new_test_view(request, subject_slug):
    if request.method == 'POST':
        form = Test_Form(request.POST)
        if form.is_valid():
            #TODO do not create test from form, get values from form and create Test object.
            test = form.save()
            test.refresh_from_db()
            subject = get_object_or_404(Subject, slug=subject_slug)
            test.subject = subject
            test.save()
            return redirect('/add_test/' + test.slug)
    else:
        form = Test_Form()

    return render(
        request, 
        'learnProgramming/add_new_test.html', 
        {
            'form': form
        }
    )