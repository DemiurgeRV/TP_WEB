from django.http import HttpResponse
from django.shortcuts import render

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
def index(request):
    return render(request, 'index.html', context={'questions': questions,
                                                  'tags': tags})

def hot(request):
    return render(request, 'hot.html', context={'questions': questions,
                                                'tags': tags})

def tag(request, tag_name):
    return render(request, 'tag.html', context={'questions': questions, 'tags': tags,
                                                'item': tag_name})
