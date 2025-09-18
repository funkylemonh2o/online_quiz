from django.contrib import admin
from .models import QuizInfo, Question, Answer


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 2  # how many empty answers to show by default


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1


@admin.register(QuizInfo)
class QuizInfoAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_by', 'created_at')
    inlines = [QuestionInline]


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'quiz')
    inlines = [AnswerInline]


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('text', 'question', 'is_correct')
