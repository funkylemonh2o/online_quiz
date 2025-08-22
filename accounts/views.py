from django.shortcuts import render

from quiz.models import QuizInfo



# Create your views here.
def main_view(request):

    quizzes = QuizInfo.objects.all()
    return render(request, "main_page.html", {"quizzes": quizzes})
