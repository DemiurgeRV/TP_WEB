from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import redirect
from .forms import CustomUserCreationForm, QuestionForm, AnswerForm, ProfileSettingsForm
from .utils import paginate
from .models import Question, Tag, Answer, Profile

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
        'tags': all_tags,
    })


@login_required
def question(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    answers = question.answers.all().order_by('-created_at')
    form = AnswerForm()

    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = Answer.objects.create(
                text=form.cleaned_data['text'],
                author=request.user.profile,
                question=question
            )
            return redirect(f"{question.get_url()}#answer-{answer.id}")

    page = paginate(answers, request)
    return render(request, 'question.html', {
        'question': question,
        'page': page,
        'form': form,
        'tags': Tag.objects.all(),
    })

@login_required
def ask(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            profile = request.user.profile
            question = Question.objects.create(
                title=form.cleaned_data['title'],
                text=form.cleaned_data['text'],
                author=profile
            )
            tags = form.cleaned_data['tags'].split()
            for tag_name in tags:
                tag, created = Tag.objects.get_or_create(name=tag_name)
                question.tags.add(tag)
            return redirect(question.get_url())
    else:
        form = QuestionForm()
    return render(request, 'ask.html', {'form': form, 'tags': Tag.objects.all()})

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            avatar = form.cleaned_data.get('avatar')
            nickname = form.cleaned_data.get('nickname')
            Profile.objects.create(user=user, avatar=avatar)
            auth_login(request, user)
            return redirect('index')
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})


def login_view(request):
    next_url = request.GET.get('continue', '/')
    error = ''
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return HttpResponseRedirect(next_url)
        else:
            error = 'Неверный логин или пароль'
    return render(request, 'login.html', {'error': error})

def logout_view(request):
    logout(request)
    return redirect(request.META.get('HTTP_REFERER', '/'))

@login_required
def settings(request):
    user = request.user
    profile = user.profile

    if request.method == 'POST':
        form = ProfileSettingsForm(request.POST, request.FILES)
        if form.is_valid():
            user.email = form.cleaned_data['email']
            profile.avatar = form.cleaned_data.get('avatar') or profile.avatar
            profile.save()
            user.save()

            password = form.cleaned_data['password']
            if password:
                user.set_password(password)
                user.save()
                update_session_auth_hash(request, user)  # 🔒 сохраняем сессию

            return redirect('settings')
    else:
        form = ProfileSettingsForm(initial={
            'nickname': user.username,
            'email': user.email,
        })

    return render(request, 'settings.html', {'form': form, 'tags': Tag.objects.all()})
