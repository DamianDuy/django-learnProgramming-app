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
        fields = ('name', 'test_description',)

class Question_Form(forms.Form):
    question_content = forms.CharField(label="Question", widget=forms.Textarea(attrs={'rows':3}), required=True)
    max_points = forms.IntegerField(label="Max points", required=True)
    multi_selection = forms.BooleanField(label="Multi-selection question", required=False)

    answer1 = forms.CharField(widget=forms.Textarea(attrs={'rows':1}), required=False)
    answer1_correct = forms.BooleanField(required=False)

    answer2 = forms.CharField(widget=forms.Textarea(attrs={'rows':1}), required=False)
    answer2_correct = forms.BooleanField(required=False)

    answer3 = forms.CharField(widget=forms.Textarea(attrs={'rows':1}), required=False)
    answer3_correct = forms.BooleanField(required=False)

    answer4 = forms.CharField(widget=forms.Textarea(attrs={'rows':1}), required=False)
    answer4_correct = forms.BooleanField(required=False)

    answer5 = forms.CharField(widget=forms.Textarea(attrs={'rows':1}), required=False)
    answer5_correct = forms.BooleanField(required=False)

    answer6 = forms.CharField(widget=forms.Textarea(attrs={'rows':1}), required=False)
    answer6_correct = forms.BooleanField(required=False)

    answer7 = forms.CharField(widget=forms.Textarea(attrs={'rows':1}), required=False)
    answer7_correct = forms.BooleanField(required=False)

    answer8 = forms.CharField(widget=forms.Textarea(attrs={'rows':1}), required=False)
    answer8_correct = forms.BooleanField(required=False)

    answer9 = forms.CharField(widget=forms.Textarea(attrs={'rows':1}), required=False)
    answer9_correct = forms.BooleanField(required=False)

    answer10 = forms.CharField(widget=forms.Textarea(attrs={'rows':1}), required=False)
    answer10_correct = forms.BooleanField(required=False)

class Answer_Form(forms.Form):
    answer1 = forms.BooleanField(required=False)
    answer2 = forms.BooleanField(required=False)
    answer3 = forms.BooleanField(required=False)
    answer4 = forms.BooleanField(required=False)
    answer5 = forms.BooleanField(required=False)
    answer6 = forms.BooleanField(required=False)
    answer7 = forms.BooleanField(required=False)
    answer8 = forms.BooleanField(required=False)
    answer9 = forms.BooleanField(required=False)
    answer10 = forms.BooleanField(required=False)