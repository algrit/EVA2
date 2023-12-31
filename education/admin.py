from django.contrib import admin

from .models import Question, Test, Course


class QTCReprModelAdmin(admin.ModelAdmin):
    """Defines representation for Questions, Tests and Courses Models"""
    list_display = ['title']
    ordering = ['id']
    list_per_page = 10


@admin.register(Question)
class QuestionAdmin(QTCReprModelAdmin):
    list_display = ['title', 'question_text', 'correct_answer', 'incorrect_answer1', 'incorrect_answer2', 'comment']
    fields = ['title', 'question_text', 'correct_answer']


@admin.register(Test)
class TestAdmin(QTCReprModelAdmin):
    filter_horizontal = ['questions']


@admin.register(Course)
class CourseAdmin(QTCReprModelAdmin):
    filter_horizontal = ['tests']
