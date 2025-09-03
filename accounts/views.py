from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from quiz.models import QuizInfo
from accounts.forms import RegisterForm, LoginForm


# Create your views here.
def main_view(request):

    quizzes = QuizInfo.objects.all()
    return render(request, "main_page.html", {"quizzes": quizzes})

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('profile')
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')