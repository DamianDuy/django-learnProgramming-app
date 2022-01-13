from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from learnProgramming.models import User_Answer
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm

from .forms import UserForm
from .forms import SignUpForm
from .forms import DeleteAccountForm

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('programming_language_list_view')
    else:
        form = SignUpForm()
    context = {'form': form}
    return render(request, 'registration/signup.html', context)

@login_required(login_url="/login/")
def show_profile(request):
    user = get_object_or_404(User, username=request.user)
    context = {'User': user}
    return render(request, "user/profile.html", context)

@login_required(login_url="/login/")
def editUser(request):
    user = get_object_or_404(User, username=request.user)
    if request.method == "POST":
        user_form = UserForm(request.POST)
        if user_form.is_valid():
            first_name = user_form.cleaned_data["first_name"]
            last_name = user_form.cleaned_data["last_name"]
            email = user_form.cleaned_data["email"]  
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.save()                           
            return redirect("/user/profile")
      
    else:
        user_form = UserForm(instance=user)
    
    context = {"User_Form": user_form,
               'messages' : messages.get_messages(request),}
    
    return render(request, "user/edit_user.html", context)

@login_required(login_url="/login/")
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('ChangePassword')
        else:
            messages.error(request, 'Please correct the error below')
    else:
        form = PasswordChangeForm(request.user)
    
    context = {"Password_Form": form,
               'messages' : messages.get_messages(request),}
    
    return render(request, 'user/change_password.html', context)

@login_required(login_url="/login/")
def delete_account(request):
    if request.method == 'POST':
        form = DeleteAccountForm(request.POST)
        if form.is_valid():
              user = get_object_or_404(User, username=request.user)
              username = form.cleaned_data["username"]
              notification = form.cleaned_data["notification"]
              if user.username == username:
                  if notification == True:
                      user.delete()
                      return redirect("/")
                  else:
                      messages.error(request, 'You did not consent to delete your account')
              else:
                  messages.error(request, 'Username is not correct')
    else:
        form = DeleteAccountForm()
       
    context = {"Delete_Account_Form": form,
               'messages' : messages.get_messages(request),}
    
    return render(request, 'user/delete_account.html', context)

@login_required(login_url="/login/")
def display_all_profiles(request):
    user = get_object_or_404(User, username=request.user)
    if user.is_superuser:
        users = User.objects.all()
    else:
        users = None
    
    context = {"Users": users}
    
    return render(request, "user/display_profiles.html", context)

def time_chart(request):
    labels = []
    data = []

    user_answer = User_Answer.objects.filter(user=request.user).order_by('-answer_time')
    user_answer_6 = user_answer[:6]
    for answer in user_answer:
        labels.append(answer.question.question_content)
        data.append(answer.answer_time)

    context = {
        'data': user_answer,
    }
    
    return render(request, 'user/statistics.html', context)
