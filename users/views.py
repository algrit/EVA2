from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render

from .forms import UserRegisterForm


def register(request):
    """It's a common view function, but I decided to add low-level authenticate just after registration
    High-level authenticate based on built-in classes is in education/view.py"""
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = request.cleaned_data['username']
            password = request.cleaned_data['password1']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/users/success/')
            else:
                return HttpResponse('SOMETHING WRONG IN USER AUTH')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', context={'form': form})


def register_success(request):
    username = request.user
    return render(request, 'users/success.html', context={'username': username})
