from django.contrib.auth import login, authenticate
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import ListView, DetailView

from users.forms import ModalLoginForm
from .models import Course, Test


def index(request):
    if request.method == 'POST':
        login_form = ModalLoginForm(request.POST)
        if login_form.is_valid():
            user = authenticate(
                username=request.POST['username'],
                password=request.POST['password'],
            )
            if user is not None:
                login(request, user)
            else:
                return render(request, 'users/login.html')
    else:
        login_form = ModalLoginForm()
    return render(request, 'education/index.html', context={'form': login_form})


class CoursesListView(ListView):
    model = Course
    template_name = 'education/courses_list.html'


class CourseDetailView(DetailView):
    model = Course
    template_name = 'education/course_detail.html'


class TestsListView(ListView):
    model = Test
    template_name = 'education/tests_list.html'


class TestDetailView(DetailView):
    model = Test
    template_name = 'education/test_detail.html'
