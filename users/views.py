from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.shortcuts import render

from .forms import UserRegisterForm


def register(request):
    """It's a common view function, but I decided to add low-level authenticate just after registration
    High-level authenticate based on built-in classes is in education/view.py"""
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = request.POST['username']
            password = request.POST['password1']
            user = authenticate(request, username=username, password=password)
            login(request, user)
            return HttpResponseRedirect('/users/success/')
    else:
        form = UserRegisterForm()
    return render(request, 'registration/register.html', context={'form': form})


def register_success(request):
    username = request.user
    return render(request, 'registration/success.html', context={'username': username})
