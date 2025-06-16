from django.http import HttpResponse
from django.shortcuts import render
from .utils import paginate

questions = []
for i in range(1,30):
    questions.append({
        'title': 'Как работает шаблонизация Django? ' + str(i),
        'id': i,
        'text':  str(i) + ''' Lorem ipsum dolor sit amet, consectetur adipiscing elit,
                              sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
                              Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris...'''
    })

tags = []
for i in range(1,16):
    tags.append({
        'name': 'Tag ' + str(i),
        'id': i,
    })

# Create your views here.
# def index(request):
#     return render(request, 'index.html', context={'questions': questions,
#                                                   'tags': tags})
#
# def hot(request):
#     return render(request, 'hot.html', context={'questions': questions,
#                                                 'tags': tags})
#
# def tag(request, tag_name):
#     return render(request, 'tag.html', context={'questions': questions, 'tags': tags,
#                                                 'item': tag_name})

def index(request):
    page = paginate(questions, request)
    return render(request, 'index.html', {'page': page, 'tags': tags})

def hot(request):
    page = paginate(questions, request)
    return render(request, 'hot.html', {'page': page, 'tags': tags})

def tag(request, tag_name):
    page = paginate(questions, request)
    return render(request, 'tag.html', {'page': page, 'tags': tags, 'item': tag_name})

def question(request, question_id):
    return render(request, 'question.html', context={'question': questions[question_id], 'tags': tags})

def ask(request):
    return render(request, 'ask.html', context={'questions': questions,
                                                  'tags': tags})

def signup(request):
    return render(request, 'signup.html')

def login(request):
    return render(request, 'login.html')

def settings(request):
    return render(request, 'settings.html')