from django.shortcuts import render
from django.core.paginator import Paginator

# Create your views here.
 
ANSWERS = [[0] * 10 for k in range(10)]
for i in range(10):
    for j in range(10):
        ANSWERS[i][j] = {
            'id': j,
            'content': f'Long lorem ipsum {j}'
        }

QUESTIONS = []
for i in range(10):
    QUESTIONS.append({
        'id': i,
        'title': f'Question {i}',
        'content': f'Long lorem ipsum {i}',
        'answer_amount': f'{len(ANSWERS[i])}'
    })

    

def paginate(request, objects, per_page=3):
    paginator = Paginator(objects, per_page)
    page = request.GET.get('page', 1)
    page_items = paginator.page(page).object_list
    return page_items



def index(request):
    return render(request, 'index.html', {'questions': paginate(request, QUESTIONS)})


def question(request, question_id):
    item = QUESTIONS[question_id]
    return render(request, 'question.html', {'question': item, 'answers': paginate(request, ANSWERS[question_id])})



def ask(request):
    return render(request, 'ask.html')

def login(request):
    return render(request, 'login.html')

def settings(request):
    return render(request, 'settings.html')

def signup(request):
    return render(request, 'signup.html')

def tag(request):
    return render(request, 'tag.html')