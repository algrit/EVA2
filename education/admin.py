from django.contrib import admin

from .models import Question, Test, Course, CourseSubscription, Content, TestAttempt, QuestionAttempt


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


@admin.register(Content)
class ContentAdmin(QTCReprModelAdmin):
    list_display = ['title', 'course', 'create_time']


@admin.register(CourseSubscription)
class CourseSubscriptionAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'course', 'course_score', 'course_passed', 'sub_time', 'unsub_time', 'update_time',
                    'active']
    ordering = ['id']
    list_per_page = 10


@admin.register(TestAttempt)
class TestAttemptAdmin(admin.ModelAdmin):
    list_display = ['id', 'course_attempt', 'test', 'test_score', 'test_passed', 'active']
    ordering = ['id']
    list_per_page = 10

@admin.register(QuestionAttempt)
class QuestionAttemptAdmin(admin.ModelAdmin):
    list_display = ['id', 'test_attempt', 'question', 'question_passed']
    ordering = ['id']
    list_per_page = 10