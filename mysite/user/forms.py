from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe

class SignUpForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', )

class UserForm(forms.ModelForm):
    
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name')

class DeleteAccountForm(forms.Form):
    username = forms.CharField()
    notification = forms.BooleanField(label=mark_safe("I wish to delete my account"))