from django.utils import timezone
import time

from django import forms
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import *
from .forms import Programming_Language_Form, Subject_Form, Test_Form, Question_Form, Answer_Form, Answer_Form_Radio

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
            'messages': messages.get_messages(request),
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
            threshold = form.cleaned_data['threshold']
            questions_number = form.cleaned_data['questions_number']
            subject = get_object_or_404(Subject, slug=subject_slug)
            test, created = Test.objects.get_or_create( name=name, subject=subject, test_description=test_description)

            if not created:
                messages.error(request, 'Test with the provided name already exists. Create a new one.')
            else:
                test.author = request.user
                test.threshold = threshold
                test.questions_number = questions_number
                test.save()
                return redirect('/edit_test/' + test.slug)
    else:
        form = Test_Form()

    return render(
        request, 
        'learnProgramming/add_new_test.html', 
        {
            'form': form,
            'messages': messages.get_messages(request),
        }
    )

@login_required(login_url='/login/')
def edit_test_info_view(request, test_id):
    if can_create(request.user) == False:
        return redirect("/no_access")

    test = get_object_or_404(Test, id=test_id)

    if request.method == 'POST':
        form = Test_Form(request.POST)
        if form.is_valid():
            test.name = form.cleaned_data['name']
            test.test_description = form.cleaned_data['test_description']
            test.threshold = form.cleaned_data['threshold']
            test.questions_number = form.cleaned_data['questions_number']
            test.save()

            return redirect('/edit_test/' + test.slug)
    else:
        initial={
            'name': test.name,
            'test_description': test.test_description,
            'threshold': test.threshold,
            'questions_number': test.questions_number,
        }
 
        form = Test_Form(initial=initial)

    return render(
        request, 
        'learnProgramming/edit_test_info.html', 
        {
            'form': form,
            'messages': messages.get_messages(request),
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
            'messages': messages.get_messages(request),
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
            'messages': messages.get_messages(request),
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
            'messages': messages.get_messages(request),
        }
    )

@login_required(login_url='/login/')
def delete_question_view(request, question_id):
    if can_create(request.user) == False:
        return redirect("/no_access")

    question = get_object_or_404(Question, id=question_id)
    path = '/edit_test/' + question.test.slug
    question.delete()

    return redirect(path)

@login_required(login_url='/login/')
def test_view(request, test_slug):
    test = get_object_or_404(Test, slug=test_slug)

    return render(
        request, 
        'learnProgramming/test.html', 
        {
            'test' : test,
            'messages': messages.get_messages(request),
        }
    )

def redirect_to_next_question_or_end(request, test, test_counter):
    global start_time
    start_time = time.time()
    user_answers = User_Answer.objects.filter(user=request.user, question__test=test, answer=None, answered=False, test_counter=test_counter)[:1]
    if user_answers.count() == 0:
        return redirect('/solved_test/' + test.slug + "/" + str(test_counter.id))
    return redirect('/solve_test/' + test.slug + "/" + str(test_counter.id) + "/" + str(user_answers[0].question.id))

def get_free_test_number(user, test):
    return Test_Counter.objects.filter(user=user, test=test).count() + 1

def question_feeder(test):
    questions = Question.objects.filter(test=test).order_by('question_number')
    number = test.questions_number
    if questions.count() < number:
        number = questions.count()
    return random.sample(list(questions), number)

@login_required(login_url='/login/')
def start_test_view(request, test_slug):
    global start_time
    start_time = time.time()
    test = get_object_or_404(Test, slug=test_slug)

    test_counter, test_counter_created = Test_Counter.objects.get_or_create(user=request.user, test=test, counter=get_free_test_number(request.user, test))

    questions = question_feeder(test)
    for question in questions:
        user_answer, created = User_Answer.objects.get_or_create(user=request.user, question=question, test_counter=test_counter)
        if not created:
            print("ERROR: this should be created!")

    return redirect_to_next_question_or_end(request, test, test_counter)

@login_required(login_url='/login/')
def solve_test_view(request, test_slug, test_counter_id, question_id):
    test = get_object_or_404(Test, slug=test_slug)
    question = get_object_or_404(Question, id=question_id)
    test_counter = get_object_or_404(Test_Counter, id=test_counter_id)

    user_answers_count = User_Answer.objects.filter(user=request.user, question__test=test, answered=True, test_counter=test_counter).count()
    print(user_answers_count)

    user_answers = User_Answer.objects.filter(user=request.user, question__test=test, answer=None, answered=False, test_counter=test_counter)
    if user_answers.count() == 0:
        return redirect('/solved_test/' + test.slug + "/" + str(test_counter.id))

    if request.method == 'POST':
        if question.multi_selection:
            form = Answer_Form(request.POST)
            if form.is_valid():
                user_answer =  User_Answer.objects.get(user=request.user, question=question, answer=None, answered=False, test_counter=test_counter)
                user_answer.answered = True
                answers = Answer.objects.filter(question=question)
                for counter, answer in enumerate(answers):
                    field_name = "answer" + str(counter+1)
                    if form.cleaned_data[field_name]:
                        user_answer.answer.add(answer)
                user_answer.answer_date = timezone.now()
                user_answer.answer_time = round(time.time() - start_time, 2)
                user_answer.save()
                return redirect_to_next_question_or_end(request, test, test_counter)
        else:
            choices = []
            answers = Answer.objects.filter(question=question).order_by("id")
            for answer in answers:
                choices.append((str(answer.id), answer.answer_content))

            form = Answer_Form_Radio(choices, request.POST)
            if form.is_valid():
                answer_id = form.cleaned_data["answer"]
                user_answer = User_Answer.objects.get(user=request.user, question=question, answer=None, answered=False, test_counter=test_counter)
                user_answer.answered = True
                user_answer.answer.add(Answer.objects.get(id=int(answer_id)))
                user_answer.answer_date = timezone.now()
                user_answer.answer_time = round(time.time() - start_time, 2)
                user_answer.save()
                return redirect_to_next_question_or_end(request, test, test_counter)
                
    else:
        answers = Answer.objects.filter(question=question).order_by("id")
        if question.multi_selection:
            form = Answer_Form()
            counter = 1
            for answer in answers:
                field_name = "answer" + str(counter)
                form.fields[field_name].label = answer.answer_content
                counter = counter + 1

            for index in range(counter, 11, 1):
                field_name = "answer" + str(index)
                form.fields[field_name].widget = forms.HiddenInput()
        else:
            choices = []
            for answer in answers:
                choices.append((str(answer.id), answer.answer_content))
            form = Answer_Form_Radio(choices=choices)

    return render(
        request, 
        'learnProgramming/solve_test.html', 
        {
            'form': form,
            'number': user_answers_count + 1,
            'question': question,
            'messages': messages.get_messages(request),
        }
    )

def get_correct_answer_number(question):
    return Answer.objects.filter(question=question, if_correct=True).count()

def get_points(user, test, test_counter):
    user_answers = User_Answer.objects.filter(user=user, question__test=test, test_counter=test_counter)
    user_points = 0
    test_points = 0
    failed_questions = []
    for user_answer in user_answers:
        question_point = user_answer.question.max_points
        test_points += question_point
        if user_answer.answered:
            if user_answer.question.multi_selection:
                correct_answers_number = get_correct_answer_number(user_answer.question)
                user_correct_answers_number = 0
                for answer in user_answer.answer.all():
                    if answer.if_correct:
                        user_correct_answers_number += 1
                    else:
                        user_correct_answers_number -= 1
                if correct_answers_number == user_correct_answers_number:
                    user_points += question_point
                else:
                    failed_questions.append(user_answer.answer.all()[0].question)
            else:
                if user_answer.answer.all()[0].if_correct:
                    user_points += question_point
                else:
                    failed_questions.append(user_answer.answer.all()[0].question)
    return user_points, test_points, failed_questions

def check_if_test_passed(user_points, test_points, threshold):
    user_result = int(100*user_points/test_points)
    if user_result >= threshold:
        return True, user_result
    return False, user_result

@login_required(login_url='/login/')
def solved_test_view(request, test_slug, test_counter_id):
    test = get_object_or_404(Test, slug=test_slug)
    test_counter = get_object_or_404(Test_Counter, id=test_counter_id)

    user_points, test_points, failed_questions = get_points(request.user, test, test_counter)
    test_status, user_result = check_if_test_passed(user_points, test_points, test.threshold)

    return render(
        request, 
        'learnProgramming/solved_test.html', 
        {
            'test': test,
            'user_points': user_points,
            'test_points': test_points,
            'test_status': test_status,
            'user_result': user_result,
            'failed_questions': failed_questions,
        }
    )