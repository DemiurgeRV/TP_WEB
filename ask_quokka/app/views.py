from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from .utils import paginate
from .models import Question, Tag, Answer

# questions = []
# for i in range(1,30):
#     questions.append({
#         'title': 'Как работает шаблонизация Django? ' + str(i),
#         'id': i,
#         'text':  str(i) + ''' Lorem ipsum dolor sit amet, consectetur adipiscing elit,
#                               sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
#                               Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris...'''
#     })
#
# tags = []
# for i in range(1,16):
#     tags.append({
#         'name': 'Tag ' + str(i),
#         'id': i,
#     })

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

# def index(request):
#     page = paginate(questions, request)
#     return render(request, 'index.html', {'page': page, 'tags': tags})
#
# def hot(request):
#     page = paginate(questions, request)
#     return render(request, 'hot.html', {'page': page, 'tags': tags})

# def tag(request, tag_name):
#     page = paginate(questions, request)
#     return render(request, 'tag.html', {'page': page, 'tags': tags, 'item': tag_name})
# def question(request, question_id):
#     return render(request, 'question.html', context={'question': questions[question_id], 'tags': tags})

def index(request):
    questions = Question.objects.new()
    page = paginate(questions, request)
    tags = Tag.objects.all()
    return render(request, 'index.html', {'page': page, 'tags': tags})

def hot(request):
    questions = Question.objects.hot()
    page = paginate(questions, request)
    tags = Tag.objects.all()
    return render(request, 'hot.html', {'page': page, 'tags': tags})

def tag(request, tag_name):
    tag = get_object_or_404(Tag, name=tag_name)
    questions = tag.questions.all()
    page = paginate(questions, request)
    all_tags = Tag.objects.all()
    return render(request, 'tag.html', {
        'page': page,
        'tag': tag,
        'item': tag.name,
        'tags': all_tags,  # <-- добавлено
    })

def question(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    answers = Answer.objects.filter(question=question).order_by('-created_at')  # или другой порядок
    page = paginate(answers, request)
    return render(request, 'question.html', {
        'question': question,
        'page': page
    })

def ask(request):
    return render(request, 'ask.html', context={'questions': questions,
                                                  'tags': tags})

def signup(request):
    return render(request, 'signup.html')

def login(request):
    return render(request, 'login.html')

def settings(request):
    return render(request, 'settings.html')