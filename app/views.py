from django.shortcuts import render
from . import models

# Create your views here.

TAGS = list(models.Tag.objects.all())[0:7]
MEMBERS = list(models.Profile.objects.all())[0:5]


def index(request):
    questions = models.paginate(request, models.Question.objects.get_new())['items']
    page_obj = models.paginate(request, models.Question.objects.get_new())['obj']
    return render(request, 'index.html', {'questions': questions, 'page_obj': page_obj, 'tags': TAGS, 'members': MEMBERS})

def question(request, question_id):
    item = models.Question.objects.all()[question_id-1]
    answers = models.paginate(request, models.Answer.objects.get_answers(item))['items']
    page_obj = models.paginate(request, models.Answer.objects.get_answers(item))['obj']
    return render(request, 'question.html', {'question': item, 'answers': answers, 'page_obj': page_obj, 'tags': TAGS, 'members': MEMBERS})

def tag(request, tag_name):
    questions = models.paginate(request, models.Question.objects.get_tag(tag_name))['items']
    page_obj = models.paginate(request, models.Question.objects.get_tag(tag_name))['obj']
    return render(request, 'tag.html', {'tag': tag_name, 'questions': questions, 'page_obj': page_obj, 'tags': TAGS, 'members': MEMBERS})

def hot(request):
    questions = models.paginate(request, models.Question.objects.get_hot())['items']
    page_obj = models.paginate(request, models.Question.objects.get_hot())['obj']
    return render(request, 'hot.html', {'questions': questions, 'page_obj': page_obj, 'tags': TAGS, 'members': MEMBERS})

def ask(request):
    return render(request, 'ask.html', {'tags': TAGS, 'members': MEMBERS})

def login(request):
    return render(request, 'login.html', {'tags': TAGS, 'members': MEMBERS})

def settings(request):
    return render(request, 'settings.html', {'tags': TAGS, 'members': MEMBERS})

def signup(request):
    return render(request, 'signup.html', {'tags': TAGS, 'members': MEMBERS})

