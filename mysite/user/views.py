from django.contrib.auth import login, authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode

from learnProgramming.models import User_Answer, Answer
from .tokens import account_activation_token

from .forms import ActivationAccountForm, UserForm
from .forms import SignUpForm
from .forms import DeleteAccountForm

def sent_email(user, current_site):
    subject = "Activate your account"
    message = render_to_string("user/account_activation_email.html", {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
    user.email_user(subject, '', html_message = message)

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():

            user = form.save(commit=False)
            user.is_active = False
            user.save()

            current_site = get_current_site(request)
            sent_email(user, current_site)

            return redirect('account_activation_sent')
    else:
        form = SignUpForm()
    context = {'form': form}
    return render(request, 'registration/signup.html', context)

def account_activation_sent(request):
    context = {'title': 'Account activation sent',
               'message': 'Email with the activation link\
                           has been sent. To activate the account\
                           click on the link.',}
    return render(request, "common/common.html", context)

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        login(request, user)
        return redirect('/')
    else:
        context = {'title': 'Account validation failed',
                   'message': 'Email activation failed.',}
        return render(request, 'common/common.html', context)

def resendEmail(request):
    if request.method == "POST":
        email_form = ActivationAccountForm(request.POST)
        if email_form.is_valid():
            email = email_form.cleaned_data["email"]  
            user = get_object_or_404(User, email=email)
                       
            current_site = get_current_site(request)
            sent_email(user, current_site)

            return redirect('account_activation_sent')
      
    else:
        email_form = ActivationAccountForm()
    
    context = {"email_form": email_form,
               'messages' : messages.get_messages(request),}
    
    return render(request, "user/account_activation_resend_email.html", context)

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

@login_required(login_url="/login/")
def statistics(request):
    return render(request, 'user/statistics.html')

@login_required(login_url="/login/")
def my_statistics(request):
    return render(request, 'user/my_statistics.html')

@login_required(login_url="/login/")
def users_statistics(request):
    return render(request, 'user/users_statistics.html')

# MY STATISTICS
@login_required(login_url="/login/")
def time_chart(request):
    labels = []
    data = []

    user_answer = User_Answer.objects.filter(user=request.user).order_by('-answer_time')
    user_answer_6 = user_answer[:6]
    for answer in user_answer_6:
        labels.append([answer.question.question_number, answer.question.test.name])
        data.append(answer.answer_time)

    context = {
        'labels': labels,
        'data': data,
    }
    
    return render(request, 'user/statistics_time-chart.html', context)

def get_correct_answer_number(question):
    return Answer.objects.filter(question=question, if_correct=True).count()

@login_required(login_url="/login/")
def correctness_chart(request):
    correct = 0 
    incorrect = 0

    user_answers = User_Answer.objects.filter(user=request.user)
    for user_answer in user_answers:
        if user_answer.answered:
            if user_answer.question.multi_selection:
                correct_answers_number = get_correct_answer_number(user_answer.question)
                user_correct_answers_number = 0
                for answer in user_answer.answer.all():
                    if answer.if_correct:
                        correct += 1
                    else:
                        incorrect +=1
            else:
                if user_answer.answer.all()[0].if_correct:
                    correct += 1
                else:
                    incorrect +=1

    context = {
        'correct': correct,
        'incorrect': incorrect,
    }
    
    return render(request, 'user/statistics_correctness-chart.html', context)

@login_required(login_url="/login/")
def test_attempt_chart(request):
    all_tests = []
    test_attempt = []

    user_answer = User_Answer.objects.filter(user=request.user)
    for answer in user_answer:
        all_tests.append(answer.question.test)

    # {testNr: number of attempt}
    test_dict = dict((x,all_tests.count(x)/x.questions_number) for x in set(all_tests))

    for t, num in test_dict.items():
        test_attempt.append([t.name, num])

    context = {
        'test_attempt': test_attempt,
    }
    
    return render(request, 'user/statistics_test_attempt-chart.html', context)

# USERS STATISTICS
@login_required(login_url="/login/")
def incorrect_answers_chart(request):
    incorrect_answers = []
    data = []

    user_answers = User_Answer.objects.all()
    for user_answer in user_answers:
        if user_answer.answered:
            if user_answer.question.multi_selection:
                correct_answers_number = get_correct_answer_number(user_answer.question)
                for answer in user_answer.answer.all():
                    if not answer.if_correct:
                        incorrect_answers.append(user_answer.question.test.name)
            else:
                if not user_answer.answer.all()[0].if_correct:
                    incorrect_answers.append(user_answer.question.test.name)


    answer_dict = {i:incorrect_answers.count(i) for i in incorrect_answers}

    for name, num in answer_dict.items():
        data.append([name, num])

    context = {
        'data': data,
    }
    
    return render(request, 'user/statistics_incorrect_answers-chart.html', context)

# statistic for how many users attempted test (only one attempt to a test)
@login_required(login_url="/login/")
def users_attempt_chart(request):
    all_tests = []
    one_attempt = []
    users_attempt = []
    tmp = []

    user_answer = User_Answer.objects.all()
    for answer in user_answer:
        all_tests.append([answer.question.test.name, answer.user.username])

    # only one attempt
    one_attempt = [list(tupl) for tupl in {tuple(i) for i in all_tests }]

    for name, user in one_attempt:
        tmp.append(name)

    users_attempt_dict = dict((x,tmp.count(x)) for x in set(tmp))

    for name, num in users_attempt_dict.items():
        users_attempt.append([name, num])

    context = {
        'users_attempt': users_attempt,
    }
    
    return render(request, 'user/statistics_users_attempt-chart.html', context)

@login_required(login_url="/login/")
def users_all_attempts_chart(request):
    all_tests = []
    test_attempt = []

    user_answer = User_Answer.objects.all()
    for answer in user_answer:
        all_tests.append(answer.question.test)

    # {testNr: number of attempt}
    test_dict = dict((x,all_tests.count(x)/x.questions_number) for x in set(all_tests))

    for t, num in test_dict.items():
        test_attempt.append([t.name, num])

    context = {
        'test_attempt': test_attempt,
    }
    
    return render(request, 'user/statistics_users_all_attempts-chart.html', context)