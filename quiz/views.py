from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from .models import QuizInfo, Question, Answer

def quiz_detail(request, pk=None):
    quizzes = QuizInfo.objects.all()
    return render(request, "quiz/quiz_detail.html", {"quizzes": quizzes})

def quiz(request, pk):
    quiz = get_object_or_404(QuizInfo, pk=pk)
    questions = list(quiz.questions.prefetch_related("answers").all())
    score = None

    if request.method == "POST":
        score = 0
        for question in questions:
            answers_qs = list(question.answers.all())
            if getattr(question, "multiple_choice", False):
                selected_raw = request.POST.getlist(f"question_{question.id}")
                selected_ids = set(int(x) for x in selected_raw if x.isdigit())
                for a in answers_qs:
                    a.is_user_selected = (a.id in selected_ids)
                correct_ids = set(a.id for a in answers_qs if a.is_correct)
                if selected_ids == correct_ids and len(correct_ids) > 0:
                    score += 1
            else:
                selected = request.POST.get(f"question_{question.id}")
                selected_id = int(selected) if selected and selected.isdigit() else None
                for a in answers_qs:
                    a.is_user_selected = (selected_id == a.id)
                if selected_id:
                    sel = next((a for a in answers_qs if a.id == selected_id), None)
                    if sel and sel.is_correct:
                        score += 1
    else:
        for question in questions:
            for a in question.answers.all():
                a.is_user_selected = False

    return render(request, "quiz/quiz.html", {
        "quiz": quiz,
        "questions": questions,
        "score": score,
    })

def search_quizzes(request):
    # read inputs
    query = (request.GET.get("search") or "").strip()
    search_by = request.GET.get("search_by", "title")

    quizzes = QuizInfo.objects.all()

    if query:
        if search_by == "description":
            quizzes = quizzes.filter(description__icontains=query)
        else:
            quizzes = quizzes.filter(title__icontains=query)

    return render(request, "quiz/quiz_detail.html", {
        "quizzes": quizzes,
        "query": query,
        "search_by": search_by,
    })

def edit(request, pk):
    quiz = get_object_or_404(QuizInfo, pk=pk, created_by=request.user)

    if request.method == "POST":
        # Always update quiz title & description safely
        title = request.POST.get("title")
        timer = request.POST.get("timer_amount")
        if title:
            quiz.title = title

        description = request.POST.get("description")
        if description is not None:
            quiz.description = description
        quiz.save()

        # Delete a question if requested
        delete_qid = request.POST.get("delete_question")
        if delete_qid:
            Question.objects.filter(id=delete_qid, quiz=quiz).delete()
            return redirect("edit", pk=quiz.pk)

        # Add new question
        new_question_text = request.POST.get("new_question")
        if new_question_text:
            multiple_choice = request.POST.get("multiple_choice") == "on"
            timer_value = request.POST.get("timer_amount")
            try:
                timer_value = int(timer_value)
            except (TypeError, ValueError):
                timer_value = 15  # default

            new_question = Question.objects.create(
                quiz=quiz,
                text=new_question_text,
                multiple_choice=multiple_choice,
                timer=timer_value
            )

            if "image" in request.FILES:
                new_question.image = request.FILES["image"]
                new_question.save()

            answer_count = int(request.POST.get("answer_count", 0))
            for i in range(answer_count):
                ans_text = request.POST.get(f"answer_{i}")
                if ans_text:
                    is_correct = str(i) in request.POST.getlist("correct_answers")
                    Answer.objects.create(
                        question=new_question,
                        text=ans_text,
                        is_correct=is_correct
                    )

        return redirect("edit", pk=quiz.pk)

    questions = quiz.questions.prefetch_related("answers").all()
    return render(request, "quiz/edit.html", {"quiz": quiz, "questions": questions})

@login_required
def delete_quiz(request, quiz_id):
    quiz = get_object_or_404(QuizInfo, id=quiz_id)
    if quiz.owner == request.user or request.user.is_staff:  # owner or admin
        quiz.delete()
    return redirect('quizzes')