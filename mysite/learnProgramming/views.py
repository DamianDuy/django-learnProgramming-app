from django.shortcuts import render
from .models import *

# Create your views here.


def index(request):
    programming_language_list = Programming_Language.objects.all()
    context = {'programming_language_list': programming_language_list}
    return render(request, 'learnProgramming/index.html', context)