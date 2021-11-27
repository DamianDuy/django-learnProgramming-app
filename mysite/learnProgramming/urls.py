"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path

from .views import programming_language_list_view, add_new_programming_language_view, delete_programming_language_view
from .views import subjects_list_view, add_new_subject_view, delete_subject_view
from .views import tests_list_view, add_new_test_view, delete_test_view, edit_test_view
from .views import add_new_question_view, edit_question_view
from .views import  about_view, no_access_view, test_view

app_name = 'learnProgramming'
urlpatterns = [
    path('', programming_language_list_view, name='programming_language_list_view'),
    path('add_new_programming_language', add_new_programming_language_view, name='add_new_programming_language_view'),
    path('delete_programming_language/<programming_lang_slug>', delete_programming_language_view, name='delete_programming_language_view'),

    path('programming_language/<programming_lang_slug>', subjects_list_view, name='subjects_list_view'),
    path('add_new_subject/<programming_lang_slug>', add_new_subject_view, name='add_new_subject_view'),
    path('delete_subject/<subject_slug>', delete_subject_view, name='delete_subject_view'),

    path('subject/<subject_slug>', tests_list_view, name='tests_list_view'),
    path('add_new_test/<subject_slug>', add_new_test_view, name='add_new_test_view'),
    path('delete_test/<test_slug>', delete_test_view, name='delete_test_view'),
    path('edit_test/<test_slug>', edit_test_view, name='edit_test_view'),

    path('add_new_question/<test_slug>', add_new_question_view, name='add_new_question_view'),
    path('edit_question/<question_id>', edit_question_view, name='edit_question_view'),

    path('about', about_view, name='about_view'),
    path('no_access', no_access_view, name='no_access_view'),
    path('test/<test_slug>', test_view, name='test_view'),
]
