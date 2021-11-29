from datetime import datetime

from django import forms
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import *
from .forms import Programming_Language_Form, Subject_Form, Test_Form, Question_Form, Answer_Form

# Create your views here.

def about_view(request):
    
    return render( 
        request, 
        'learnProgramming/about.html'
    )

def programming_language_list_view(request):
    programming_language_list = Programming_Language.objects.all()
    
    return render( 
        request, 
        'learnProgramming/index.html', 
        {
            'programming_language_list': programming_language_list
        }
    )

def subjects_list_view(request, programming_lang_slug):
    programming_lang = get_object_or_404(Programming_Language, slug=programming_lang_slug)
    subjects_list = Subject.objects.filter(programming_lang=programming_lang)

    return render(
        request,
        'learnProgramming/subjects_list.html',
        {
            'programming_lang' : programming_lang,
            'subjects_list' : subjects_list,
        }
    )

def tests_list_view(request, subject_slug):
    subject = get_object_or_404(Subject, slug=subject_slug)
    tests_list = Test.objects.filter(subject=subject)

    return render(
        request,
        'learnProgramming/tests_list.html',
        {
            'programming_lang' : subject.programming_lang,
            'subject' : subject,
            'tests_list' : tests_list,
        }
    )

def no_access_view(request):
    return render(
        request,
        'learnProgramming/no_access.html',
        {}
    )

def can_create(user:User) -> bool:
    if user.is_superuser:
        return True
    if user.profile.canCreate:
        return True
    return False

@login_required(login_url='/login/')
def add_new_programming_language_view(request):
    if can_create(request.user) == False:
        return redirect("/no_access")

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

@login_required(login_url='/login/')
def delete_programming_language_view(request, programming_lang_slug):
    if not request.user.is_superuser:
        return redirect("/no_access")

    programming_lang = get_object_or_404(Programming_Language, slug=programming_lang_slug)
    programming_lang.delete()

    return redirect("/")

@login_required(login_url='/login/')
def add_new_subject_view(request, programming_lang_slug):
    if can_create(request.user) == False:
        return redirect("/no_access")

    if request.method == 'POST':
        form = Subject_Form(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            programming_lang = get_object_or_404(Programming_Language, slug=programming_lang_slug)
            subject, created = Subject.objects.get_or_create(name=name, programming_lang=programming_lang)

            if not created:
                messages.error(request, 'Subject with the provided name already exists. Create a new one.')
            else:
                subject.author = request.user
                subject.save()
                return redirect('/subject/' + subject.slug)
            
    else:
        form = Subject_Form()

    return render(
        request, 
        'learnProgramming/add_new_subject.html', 
        {
            'form': form,
            'messages': messages,
        }
    )

@login_required(login_url='/login/')
def delete_subject_view(request, subject_slug):
    if not request.user.is_superuser:
        return redirect("/no_access")

    subject = get_object_or_404(Subject, slug=subject_slug)
    path = "/programming_language/" + subject.programming_lang.slug
    subject.delete()

    return redirect(path)

@login_required(login_url='/login/')
def add_new_test_view(request, subject_slug):
    if can_create(request.user) == False:
        return redirect("/no_access")

    if request.method == 'POST':
        form = Test_Form(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            test_description = form.cleaned_data['test_description']
            subject = get_object_or_404(Subject, slug=subject_slug)
            test, created = Test.objects.get_or_create( name=name, subject=subject, test_description=test_description)

            if not created:
                messages.error(request, 'Test with the provided name already exists. Create a new one.')
            else:
                test.author = request.user
                test.save()
                return redirect('/edit_test/' + test.slug)
    else:
        form = Test_Form()

    return render(
        request, 
        'learnProgramming/add_new_test.html', 
        {
            'form': form,
            'message': messages,
        }
    )

@login_required(login_url='/login/')
def delete_test_view(request, test_slug):
    if not request.user.is_superuser:
        return redirect("/no_access")

    test = get_object_or_404(Test, slug=test_slug)
    path = "/subject/" + test.subject.slug
    test.delete()

    return redirect(path)

@login_required(login_url='/login/')
def edit_test_view(request, test_slug):
    if can_create(request.user) == False:
        return redirect("/no_access")

    test = get_object_or_404(Test, slug=test_slug)

    questions = Question.objects.filter( test=test).order_by('question_number')

    return render(
        request, 
        'learnProgramming/edit_test.html', 
        {
            'test': test,
            'questions': questions,
            'message': messages,
        }
    )

def get_next_free_question_number(test:Test) -> int:
    questions_number = Question.objects.filter(test=test).count()
    return questions_number+1

def is_only_one_answer_correct(elem_list) -> bool:
    counter = 0
    for elem in elem_list:
        counter = counter + 1 if elem == True else counter

    if counter == 1:
        return True
    
    return False

def is_at_least_one_answer_correct(elem_list) -> bool:
    counter = 0
    for elem in elem_list:
        counter = counter + 1 if elem == True else counter

    if counter > 0:
        return True
    
    return False

@login_required(login_url='/login/')
def add_new_question_view(request, test_slug):
    if can_create(request.user) == False:
        return redirect("/no_access")

    test = get_object_or_404(Test, slug=test_slug)

    if request.method == 'POST':
        form = Question_Form(request.POST)
        if form.is_valid():
            question_number = get_next_free_question_number(test)
            question_content = form.cleaned_data['question_content']
            max_points = form.cleaned_data['max_points']
            multi_selection = form.cleaned_data['multi_selection']

            answers_list=[]

            answer1 = form.cleaned_data['answer1']
            answer1_correct = form.cleaned_data['answer1_correct']
            answers_list.append((answer1, answer1_correct))

            answer2 = form.cleaned_data['answer2']
            answer2_correct = form.cleaned_data['answer2_correct']
            answers_list.append((answer2, answer2_correct))

            answer3 = form.cleaned_data['answer3']
            answer3_correct = form.cleaned_data['answer3_correct']
            answers_list.append((answer3, answer3_correct))

            answer4 = form.cleaned_data['answer4']
            answer4_correct = form.cleaned_data['answer4_correct']
            answers_list.append((answer4, answer4_correct))

            answer5 = form.cleaned_data['answer5']
            answer5_correct = form.cleaned_data['answer5_correct']
            answers_list.append((answer5, answer5_correct))

            answer6 = form.cleaned_data['answer6']
            answer6_correct = form.cleaned_data['answer6_correct']
            answers_list.append((answer6, answer6_correct))

            answer7 = form.cleaned_data['answer7']
            answer7_correct = form.cleaned_data['answer7_correct']
            answers_list.append((answer7, answer7_correct))

            answer8 = form.cleaned_data['answer8']
            answer8_correct = form.cleaned_data['answer8_correct']
            answers_list.append((answer8, answer8_correct))

            answer9 = form.cleaned_data['answer9']
            answer9_correct = form.cleaned_data['answer9_correct']
            answers_list.append((answer9, answer9_correct))

            answer10 = form.cleaned_data['answer10']
            answer10_correct = form.cleaned_data['answer10_correct']
            answers_list.append((answer10, answer10_correct))

            flag = True

            if multi_selection == False:
                if not is_only_one_answer_correct([answer1_correct, answer2_correct, answer3_correct, answer4_correct, answer5_correct, answer6_correct, answer7_correct, answer8_correct, answer9_correct, answer10_correct]):
                    flag = False
                    messages.error(request, 'Make sure that only one answer is correct.')
            else:
                if not is_at_least_one_answer_correct([answer1_correct, answer2_correct, answer3_correct, answer4_correct, answer5_correct, answer6_correct, answer7_correct, answer8_correct, answer9_correct, answer10_correct]):
                    flag = False
                    messages.error(request, 'Make sure that at least one answer is correct.')

            if flag:
                question, question_created = Question.objects.get_or_create(
                    question_number=question_number,
                    question_content=question_content,
                    max_points=max_points,
                    test=test,
                    multi_selection=multi_selection
                )

                for elem in answers_list:
                    if elem[0] != "":
                        answer_object, answer_created = Answer.objects.get_or_create(
                            answer_content=elem[0],
                            question=question,
                            if_correct=elem[1]
                        )

                if not question_created:
                    messages.error(request, 'Question with the provided paramters already exists. Create a new one.')
                else:
                    return redirect('/edit_test/' + test.slug)
    else:
        form = Question_Form()

    title = "Add a new question to " + test.name + " test."
    button_name = "Add"

    return render(
        request, 
        'learnProgramming/add_new_question.html', 
        {
            'title' : title,
            'button_name' : button_name,
            'form': form,
            'message': messages,
        }
    )

@login_required(login_url='/login/')
def edit_question_view(request, question_id):
    if can_create(request.user) == False:
        return redirect("/no_access")

    question = get_object_or_404(Question, id=question_id)

    if request.method == 'POST':
        form = Question_Form(request.POST)
        if form.is_valid():
            question_content = form.cleaned_data['question_content']
            max_points = form.cleaned_data['max_points']
            multi_selection = form.cleaned_data['multi_selection']

            answers_list=[]

            answer1 = form.cleaned_data['answer1']
            answer1_correct = form.cleaned_data['answer1_correct']
            answers_list.append((answer1, answer1_correct))

            answer2 = form.cleaned_data['answer2']
            answer2_correct = form.cleaned_data['answer2_correct']
            answers_list.append((answer2, answer2_correct))

            answer3 = form.cleaned_data['answer3']
            answer3_correct = form.cleaned_data['answer3_correct']
            answers_list.append((answer3, answer3_correct))

            answer4 = form.cleaned_data['answer4']
            answer4_correct = form.cleaned_data['answer4_correct']
            answers_list.append((answer4, answer4_correct))

            answer5 = form.cleaned_data['answer5']
            answer5_correct = form.cleaned_data['answer5_correct']
            answers_list.append((answer5, answer5_correct))

            answer6 = form.cleaned_data['answer6']
            answer6_correct = form.cleaned_data['answer6_correct']
            answers_list.append((answer6, answer6_correct))

            answer7 = form.cleaned_data['answer7']
            answer7_correct = form.cleaned_data['answer7_correct']
            answers_list.append((answer7, answer7_correct))

            answer8 = form.cleaned_data['answer8']
            answer8_correct = form.cleaned_data['answer8_correct']
            answers_list.append((answer8, answer8_correct))

            answer9 = form.cleaned_data['answer9']
            answer9_correct = form.cleaned_data['answer9_correct']
            answers_list.append((answer9, answer9_correct))

            answer10 = form.cleaned_data['answer10']
            answer10_correct = form.cleaned_data['answer10_correct']
            answers_list.append((answer10, answer10_correct))

            flag = True

            if multi_selection == False:
                if not is_only_one_answer_correct([answer1_correct, answer2_correct, answer3_correct, answer4_correct, answer5_correct, answer6_correct, answer7_correct, answer8_correct, answer9_correct, answer10_correct]):
                    flag = False
                    messages.error(request, 'Make sure that only one answer is correct.')
            else:
                if not is_at_least_one_answer_correct([answer1_correct, answer2_correct, answer3_correct, answer4_correct, answer5_correct, answer6_correct, answer7_correct, answer8_correct, answer9_correct, answer10_correct]):
                    flag = False
                    messages.error(request, 'Make sure that at least one answer is correct.')

            if flag:
                question.question_content=question_content
                question.max_points = max_points
                question.multi_selection = multi_selection
                question.save()

                answers = Answer.objects.filter(question=question).order_by("id")
                for answer in answers:
                    answer.delete()

                for elem in answers_list:
                    if elem[0] != "":
                        answer_object, answer_created = Answer.objects.get_or_create(
                            answer_content=elem[0],
                            question=question,
                            if_correct=elem[1]
                        )

                return redirect('/edit_test/' + question.test.slug)
    else:
        initial={
            'question_content': question.question_content,
            'max_points': question.max_points,
            'multi_selection': question.multi_selection,
        }
        answers = Answer.objects.filter(question=question).order_by("id")
        for index, answer in enumerate(answers):
            name = "answer"+str(index+1)
            initial[name] = answer.answer_content
            name = "answer"+str(index+1)+"_correct"
            initial[name] = answer.if_correct

        form = Question_Form(initial=initial)
        
    title = "Edit question."
    button_name = "Save"

    return render(
        request, 
        'learnProgramming/add_new_question.html', 
        {
            'title' : title,
            'button_name' : button_name,
            'form': form,
            'message': messages,
        }
    )

@login_required(login_url='/login/')
def test_view(request, test_slug):
    test = get_object_or_404(Test, slug=test_slug)

    return render(
        request, 
        'learnProgramming/test.html', 
        {
            'test' : test,
            'message': messages,
        }
    )

@login_required(login_url='/login/')
def start_test_view(request, test_slug):
    test = get_object_or_404(Test, slug=test_slug)

    questions = Question.objects.filter(test=test).order_by('question_number')[:test.questions_number]
    for question in questions:
        user_answer, created = User_Answer.objects.get_or_create(user=request.user, question=question)
        if not created:
            print("ERROR: this should be created!")

    user_answers = User_Answer.objects.filter(user=request.user, question__test=test, answer=None, answered=False)[:1]
    if user_answers.count() == 0:
        return redirect('/solved_test/' + test.slug)
    return redirect('/solve_test/' + test.slug + "/" + str(user_answers[0].question.id))

@login_required(login_url='/login/')
def solve_test_view(request, test_slug, question_id):
    test = get_object_or_404(Test, slug=test_slug)
    question = get_object_or_404(Question, id=question_id)

    user_answers = User_Answer.objects.filter(user=request.user, question__test=test, answer=None, answered=False)
    if user_answers.count() == 0:
        return redirect('/solved_test/' + test.slug)

    if request.method == 'POST':
        form = Answer_Form(request.POST)
        if form.is_valid():
            user_answer =  User_Answer.objects.get(user=request.user, question=question, answer=None, answered=False)
            user_answer.answered = True
            answers = Answer.objects.filter(question=question)
            for counter, answer in enumerate(answers):
                field_name = "answer" + str(counter+1)
                if form.cleaned_data[field_name]:
                    user_answer.answer.add(answer)
            user_answer.save()
            Answers_Data.objects.get_or_create(answer_date=datetime.now(), user_answer=user_answer)
            user_answers = User_Answer.objects.filter(user=request.user, question__test=test, answer=None, answered=False)[:1]
            if user_answers.count() == 0:
                return redirect('/solved_test/' + test.slug)
            return redirect('/solve_test/' + test.slug + "/" + str(user_answers[0].question.id))
    else:
        form = Answer_Form()
        answers = Answer.objects.filter(question=question)
        counter = 1
        for answer in answers:
            field_name = "answer" + str(counter)
            form.fields[field_name].label = answer.answer_content
            counter = counter + 1

        for index in range(counter, 11, 1):
            field_name = "answer" + str(index)
            form.fields[field_name].widget = forms.HiddenInput()

    return render(
        request, 
        'learnProgramming/solve_test.html', 
        {
            'form': form,
            'number': test.questions_number - user_answers.count() + 1,
            'question': question,
            'message': messages,
        }
    )

@login_required(login_url='/login/')
def solved_test_view(request, test_slug):
    test = get_object_or_404(Test, slug=test_slug)

    return render(
        request, 
        'learnProgramming/solved_test.html', 
        {
            'test': test,
        }
    )