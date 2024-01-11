from django.contrib.auth import login, authenticate
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from education.models import Course, CourseSubscription
from users.forms import ModalLoginForm
from django.views.generic import ListView


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


# class CoursesListView(ListView):
#     model = Course
#     template_name = 'education/all_courses_list.html'

@login_required(login_url='/users/login/')
def subscribe(request):
    user = request.user
    courses = Course.objects.all()
    courses_status = {}
    for course in courses:
        try:
            courses_status[course] = CourseSubscription.objects.get(user=user, course=course, active=1)
        except CourseSubscription.DoesNotExist:
            courses_status[course] = 'unsubed'
    return render(request, 'education/all_courses_list.html', context={'courses_status': courses_status})