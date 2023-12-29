from django.contrib.auth import login, authenticate
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import ListView, DetailView

from users.forms import ModalLoginForm
from .models import Course, Test


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


class CoursesListView(ListView):
    model = Course
    template_name = 'education/subscribed_courses.html'


class CourseDetailView(DetailView):
    model = Course
    template_name = 'education/course_detail.html'


class TestsListView(ListView):
    model = Test
    template_name = 'education/tests_list.html'


class TestDetailView(DetailView):
    model = Test
    template_name = 'education/test_detail.html'
