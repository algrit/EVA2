import datetime
import time

from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render

from education.models import Course, CourseSubscription
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


@login_required(login_url='/users/login/')
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


@login_required(login_url='/users/login/')
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


@login_required(login_url='/users/login/')
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
