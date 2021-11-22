from django import forms

from .models import Programming_Language, Subject, Test

class Programming_Language_Form(forms.ModelForm):
    icon = forms.CharField(max_length=1000, required=False)
    class Meta:
        model = Programming_Language
        fields = ('name', 'icon')
    
class Subject_Form(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ('name',)

class Test_Form(forms.ModelForm):
    class Meta:
        model = Test
        fields = ('name',)