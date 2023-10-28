from django.http import HttpResponse
from django.views.generic import ListView, DetailView

from .models import Course, Test
from django.shortcuts import render
from django.contrib.auth import login, authenticate
from users.forms import LoginForm

def index(request):
    message = ''
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                message = f'Hello {user.username}! You have been logged in'
            else:
                message = 'Login failed!'
    return render(request, 'education/index.html', context={'form': form, 'message': message})


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