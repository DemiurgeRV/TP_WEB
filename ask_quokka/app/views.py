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

# Create your views here.
def index(request):
    return render(request, 'index.html', context={'questions': questions})