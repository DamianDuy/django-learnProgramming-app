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
from .views import programming_language_list_view, subjects_list_view, tests_list_view, about_view

app_name = 'learnProgramming'
urlpatterns = [
    path('', programming_language_list_view, name='programming_language_list_view'),
    path('about', about_view, name='about_view'),
    path('programming_language/<programming_lang_slug>', subjects_list_view, name='subjects_list_view'),
    path('subject/<subject_slug>', tests_list_view, name='tests_list_view'),
]
