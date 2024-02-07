import datetime

from django import forms
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import ListView, DetailView

from education.forms import QuestionForm
from education.models import Course, CourseSubscription, Content, Test, TestAttempt, Question, QuestionAttempt
from users.forms import ModalLoginForm


def index(request):
    print(request.user)
    if request.method == 'POST':
        login_form = ModalLoginForm(request,
                                    data=request.POST)  # Somehow 1st argument of AuthenticationForm have to be 'request'
        if login_form.is_valid():
            user = authenticate(
                username=login_form.cleaned_data['username'],
                password=login_form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
        else:
            return render(request, 'users/login.html', context={'form': login_form})
    else:
        login_form = ModalLoginForm()
    return render(request, 'education/index.html', context={'form': login_form, 'user': request.user})


@login_required
def all_courses(request):
    user = request.user
    courses = Course.objects.all()
    courses_status = {}
    for course in courses:
        try:
            courses_status[course] = (CourseSubscription.objects.select_related('user', 'course')
                                      .get(user=user, course=course, active=1))
        except CourseSubscription.DoesNotExist:
            courses_status[course] = 'unsubed'
    return render(request, 'education/all_courses_list.html', context={'courses_status': courses_status})


@login_required
def course_sub(request, course_id: int):
    user = request.user
    course = Course.objects.get(id=course_id)
    if CourseSubscription.objects.select_related('user', 'course').filter(
            Q(user=user) &
            Q(course=course) &
            Q(active=True)).exists():
        return HttpResponse('Subscription is not allowed! This user is already subscribed to this course.')
    sub = CourseSubscription(user=user, course=course)
    sub.save()
    return HttpResponseRedirect('/edu/courses/')


@login_required
def course_unsub(request, course_id: int):
    user = request.user
    course = Course.objects.get(id=course_id)
    try:
        unsub = CourseSubscription.objects.select_related('user', 'course').get(user=user, course=course, active=1)
    except ObjectDoesNotExist:
        return HttpResponse('Unsub is not allowed! This user is not subscribed to this course.')
    unsub.active = 0
    unsub.unsub_time = datetime.datetime.now()
    unsub.save()
    return HttpResponseRedirect('/edu/courses/')


# @login_required(login_url='/users/login/')  # old version based on func
# def my_courses(request):
#     user = request.user
#     subs = CourseSubscription.objects.filter(user=user, active=1)
#     my_courses = []
#     for sub in subs:
#         my_courses.append(sub.course)
#     return render(request, 'education/my_courses.html', context={'my_courses': my_courses})


class MyCoursesView(LoginRequiredMixin, ListView):
    context_object_name = 'my_courses'
    template_name = 'education/my_courses.html'

    def get_queryset(self):
        user = self.request.user
        # return [sub.course for sub in CourseSubscription.objects.filter(user=user, active=1).order_by("-sub_time")]
        sub_filter = Q(coursesubscription__user=user) & Q(coursesubscription__active=1)
        return Course.objects.filter(sub_filter).order_by("-coursesubscription__sub_time")


class CourseView(LoginRequiredMixin, DetailView):
    model = Course
    context_object_name = 'course'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        context['content'] = Content.objects.select_related('course').filter(course=context['course'])
        return context


@login_required
def start_test_warning(request, pk_course: int, pk_test: int):
    test_quiz = Test.objects.get(id=pk_test)
    number_of_q = len(Question.objects.filter(test__id=pk_test))
    course = Course.objects.get(id=pk_course)
    return render(request, 'education/start_test_warning.html', context={'test_quiz': test_quiz,
                                                                         'number_of_q': number_of_q,
                                                                         'course': course})


@login_required
def test_att_create(request, pk_course: int, pk_test: int):
    user = request.user
    test = Test.objects.get(id=pk_test)
    course_attempt = CourseSubscription.objects.select_related('user', 'course').get(user=user, course__id=pk_course,
                                                                                     active=1)
    test_attempt = TestAttempt(user=user, course_attempt=course_attempt, test=test)
    test_attempt.save()
    return HttpResponseRedirect((reverse('test_attempt', args=[test_attempt.id])))


def update_test_att_score(test_att, num_corrects, num_q):
    test_score = round(num_corrects / num_q * 100)
    test_att.test_score = test_score
    if test_score >= 80:
        test_att.test_passed = True
    test_att.save()


@login_required
def test_attempt(request, pk_test_attempt: int):
    test_att = TestAttempt.objects.get(id=pk_test_attempt)
    if test_att.active == 0:
        return HttpResponse('<h1>This test attempt is already ended. You can not continue it.</h1>')
    user = request.user
    form_class = QuestionForm()
    test_quiz = test_att.test
    q_list = Question.objects.filter(test__id=test_quiz.id)
    for question in q_list:
        ANSWERS = [('correct', question.correct_answer),
                   ('incorrect1', question.incorrect_answer1),
                   ('incorrect2', question.incorrect_answer2), ]
        choice_field = forms.ChoiceField(label=question.question_text, widget=forms.RadioSelect(),
                                         choices=ANSWERS)
        form_class.fields[f"{question.id}"] = choice_field

    if request.method == 'POST':
        form_class = QuestionForm(request.POST)
        if form_class.is_valid():
            test_att.end_time = datetime.datetime.now()
            test_att.active = 0
            num_corrects = 0
            for q, answer_name in dict(list(form_class.data.items())[1:]).items():
                question = Question.objects.get(id=q)
                if form_class.data[q] == 'correct':
                    QuestionAttempt(user=user, test_attempt_id=pk_test_attempt, question=question,
                                    answer=question.correct_answer, question_passed=1).save()
                    num_corrects += 1
                elif form_class.data[q] == 'incorrect1':
                    QuestionAttempt(user=user, test_attempt_id=pk_test_attempt, question=question,
                                    answer=question.incorrect_answer1, question_passed=0).save()
                else:
                    QuestionAttempt(user=user, test_attempt_id=pk_test_attempt, question=question,
                                    answer=question.incorrect_answer2, question_passed=0).save()
            update_test_att_score(test_att, num_corrects, len(q_list))

            # return HttpResponseRedirect((reverse('test_result', args=[pk_test_attempt])))
            # return HttpResponse('Its OK')
            return HttpResponseRedirect(f'/edu/my/attempt/result/{test_att.id}/')
    return render(request, 'education/test_attempt.html', context={'form': form_class})


def ugly_test_time_spent_format(end_time, start_time):
    time_spent = end_time - start_time
    day_time_list = str(time_spent).split('.')[0].split(',')
    time = day_time_list[-1].split(':')
    time_spent = f'{time[-1]} seconds'
    if len(time) > 1:
        time_spent = f'{time[-2]} minutes {time_spent}'
    if len(time) > 2:
        time_spent = f'{time[-3]} hours {time_spent}'
    if len(day_time_list) > 1:
        time_spent = f'{day_time_list[-2]} {time_spent}'
    return time_spent

@login_required
def test_att_result(request, pk_test_attempt: int):
    user = request.user
    test_att = TestAttempt.objects.get(id=pk_test_attempt)
    time_spent = ugly_test_time_spent_format(test_att.end_time, test_att.start_time)

    form_class = QuestionForm()
    return render(request, 'education/test_att_result.html', context={'test_att': test_att,
                                                                      'time_spent': time_spent})
