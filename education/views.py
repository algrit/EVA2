import datetime

from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.views.generic import ListView, DetailView

from education.models import Course, CourseSubscription, Content
from users.forms import ModalLoginForm


def index(request):
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
            courses_status[course] = CourseSubscription.objects.get(user=user, course=course, active=1)
        except CourseSubscription.DoesNotExist:
            courses_status[course] = 'unsubed'
    return render(request, 'education/all_courses_list.html', context={'courses_status': courses_status})


@login_required
def course_sub(request, course_id: int):
    user = request.user
    course = Course.objects.get(id=course_id)
    if CourseSubscription.objects.filter(
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
        unsub = CourseSubscription.objects.get(user=user, course=course, active=1)
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
        # context['tests'] = Test
        context['content'] = Content.objects.filter(course=context['course'])
        return context
