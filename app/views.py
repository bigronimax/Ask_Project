from django.shortcuts import render
from django.core.paginator import Paginator

# Create your views here.
 
TAGS = [{'name': 'Perl'}, 
        {'name': 'Python'}, 
        {'name': 'MySQL'}, 
        {'name': 'Django'}, 
        {'name': 'Mail.ru'}, 
        {'name': 'Firefox'}]

MEMBERS = [{'name': 'Mr. Freeman'}, 
           {'name': 'Dr. House'}, 
           {'name': 'Bender'}, 
           {'name': 'Walter White'},  
           {'name': 'Sam'}] 

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
        'answer_amount': f'{len(ANSWERS[i])}',
        'tags': TAGS[1:3]
    })


def paginate(request, objects, per_page=3):
    paginator = Paginator(objects, per_page)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    page_items = paginator.page(page_number).object_list
    return {'items': page_items, 'obj': page_obj}


def tag_selection(questions, tag_name):
    result = []
    for i in range(len(questions)):
        tags = questions[i]['tags']
        for j in range(len(tags)):
            if (tag_name == tags[j]['name']):
                result.append(questions[i])
    return result

#def log_out(request):
#   log = request.GET.get('log', True)
#  return log


def index(request):
    questions = paginate(request, QUESTIONS)['items']
    page_obj = paginate(request, QUESTIONS)['obj']
    return render(request, 'index.html', {'questions': questions, 'page_obj': page_obj, 'tags': TAGS, 'members': MEMBERS})

def question(request, question_id):
    item = QUESTIONS[question_id]
    answers = paginate(request, ANSWERS[question_id])['items']
    page_obj = paginate(request, ANSWERS[question_id])['obj']
    return render(request, 'question.html', {'question': item, 'answers': answers, 'page_obj': page_obj, 'tags': TAGS, 'members': MEMBERS})

def tag(request, tag_name):
    questions = paginate(request, tag_selection(QUESTIONS, tag_name))['items']
    page_obj = paginate(request, tag_selection(QUESTIONS, tag_name))['obj']
    return render(request, 'tag.html', {'tag': tag_name, 'questions': questions, 'page_obj': page_obj, 'tags': TAGS, 'members': MEMBERS})

def hot(request):
    questions = paginate(request, QUESTIONS)['items']
    page_obj = paginate(request, QUESTIONS)['obj']
    return render(request, 'hot.html', {'questions': questions, 'page_obj': page_obj, 'tags': TAGS, 'members': MEMBERS})

def ask(request):
    return render(request, 'ask.html', {'tags': TAGS, 'members': MEMBERS})

def login(request):
    return render(request, 'login.html', {'tags': TAGS, 'members': MEMBERS})

def settings(request):
    return render(request, 'settings.html', {'tags': TAGS, 'members': MEMBERS})

def signup(request):
    return render(request, 'signup.html', {'tags': TAGS, 'members': MEMBERS})

