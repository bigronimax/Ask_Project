from math import ceil
from django.contrib import auth
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from . import models
import app.forms


# Create your views here.

TAGS = list(models.Tag.objects.all())[0:7]
MEMBERS = list(models.Profile.objects.all())[0:5]

def redirect_continue(request):
    continue_href = request.GET.get('continue', '/')
    return redirect(continue_href)


@login_required(login_url="login", redirect_field_name="continue")
def index(request):
    questions = models.paginate(request, models.Question.objects.get_new())['items']
    page_obj = models.paginate(request, models.Question.objects.get_new())['obj']
    return render(request, 'index.html', {'questions': questions, 'page_obj': page_obj, 'tags': TAGS, 'members': MEMBERS})

def question(request, question_id):
    item = models.Question.objects.all()[question_id-1]
    answers = models.paginate(request, models.Answer.objects.get_answers(item))['items']
    page_obj = models.paginate(request, models.Answer.objects.get_answers(item))['obj']
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')
        answer_form = app.forms.AnswerForm(request.user, question_id, request.POST)
        if answer_form.is_valid():
            answer_form.save()
            last_page = ceil(len(models.Answer.objects.get_answers(item)) / 3)
            redirect_url = reverse('question', args=[question_id]) + f'?page={last_page}'
            return redirect(redirect_url)
    else:
        answer_form = app.forms.AnswerForm(request.user,question_id)

    return render(request, 'question.html', {'question': item, 'answers': answers, 'page_obj': page_obj, 'tags': TAGS, 'members': MEMBERS, 'form': answer_form})

def tag(request, tag_name):
    questions = models.paginate(request, models.Question.objects.get_tag(tag_name))['items']
    page_obj = models.paginate(request, models.Question.objects.get_tag(tag_name))['obj']
    return render(request, 'tag.html', {'tag': tag_name, 'questions': questions, 'page_obj': page_obj, 'tags': TAGS, 'members': MEMBERS})

def hot(request):
    questions = models.paginate(request, models.Question.objects.get_hot())['items']
    page_obj = models.paginate(request, models.Question.objects.get_hot())['obj']
    return render(request, 'hot.html', {'questions': questions, 'page_obj': page_obj, 'tags': TAGS, 'members': MEMBERS})

def ask(request):
    if request.method == 'POST':
        ask_form = app.forms.AskForm(request.user, request.POST)
        if ask_form.is_valid():
            question = ask_form.save()
            return redirect(reverse('question', args=[question.id]))
    else:
        ask_form = app.forms.AskForm(request.user)
    return render(request, 'ask.html', {'tags': TAGS, 'members': MEMBERS, 'form': ask_form})

def logout(request):
    auth.logout(request)
    return redirect(request.GET.get("continue", "index"))

def login(request):   
    if request.method == "POST":
        login_form = app.forms.LoginForm(request.POST)
        if login_form.is_valid():
            user = auth.authenticate(request, **login_form.cleaned_data)
            if user is not None:
                auth.login(request, user)
                return redirect(request.GET.get("continue", "index"))
            else:
                login_form.add_error(None, "Wrong username or password!")
    else:
        login_form = app.forms.LoginForm()
                
    return render(request, 'login.html', {'tags': TAGS, 'members': MEMBERS, 'form': login_form})

@login_required(login_url="login", redirect_field_name="continue")
def settings(request):
    if request.method == 'GET':
        edit_form = app.forms.ProfileForm(request.user)
    if request.method == 'POST':
        edit_form = app.forms.ProfileForm(request.user, request.POST)
        if edit_form.is_valid():
            edit_form.save()
    return render(request, 'settings.html', {'tags': TAGS, 'members': MEMBERS, 'form': edit_form})

def signup(request):
    if request.method == 'GET':
        user_form = app.forms.RegisterForm()
    if request.method == 'POST':
        user_form = app.forms.RegisterForm(request.POST)
        if user_form.is_valid():
            user = user_form.save()
            if user:
                auth.login(request, user)
                return redirect(reverse('index'))
            else:
                user_form.add_error(None, 'Error with creating a new account!')
    return render(request, 'signup.html', {'tags': TAGS, 'members': MEMBERS, 'form': user_form})

