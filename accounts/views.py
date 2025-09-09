from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from quiz.models import QuizInfo
from accounts.forms import RegisterForm, LoginForm


# Create your views here.
def main_view(request):
    query = request.GET.get("search")
    search_by = request.GET.get("search_by")
    quizzes = QuizInfo.objects.all()

    if query:
        if search_by == "title":
            quizzes = quizzes.filter(title__icontains=query)
        elif search_by == "description":
            quizzes = quizzes.filter(description__icontains=query)
    return render(request, "main_page.html", {"quizzes": quizzes, "query": query})


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('/')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')


def create(request):
    if request.method == "POST":
        title = request.POST.get("title")  # get title from form
        description = request.POST.get("description")  # optional if you want

        QuizInfo.objects.create(
            created_by=request.user,  # must match your model field
            title=title,
            description=description,
        )

        return redirect("main_page")  # go back to main page after creation
    return redirect("main_page")
