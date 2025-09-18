from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.conf import settings


class QuizInfo(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="quizzes"
    )

    def __str__(self):
        return self.title


class Question(models.Model):
    timer = models.IntegerField(default=15, validators=[MinValueValidator(1), MaxValueValidator(100)])
    quiz = models.ForeignKey(
        QuizInfo,
        on_delete=models.CASCADE,
        related_name="questions"
    )
    text = models.CharField(max_length=500)
    image = models.ImageField(upload_to="question_images/", blank=True, null=True)
    multiple_choice = models.BooleanField(default=False)

    def __str__(self):
        return f"Q: {self.text[:50]}"


class Answer(models.Model):
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name="answers"
    )
    text = models.CharField(max_length=300)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"Answer: {self.text[:50]} ({'Correct' if self.is_correct else 'Wrong'})"
