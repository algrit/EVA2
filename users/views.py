from django.contrib.auth import views, authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render

from .forms import UserRegisterForm, AccountSettings


def register(request):
    """It's a common view function, but I decided to add low-level authentication just after registration.
    High-level class-based authentication (LoginView) is in urls.py"""
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/users/success/')
            else:
                return HttpResponse('SOMETHING WRONG IN USER AUTH')  # didn't find the way it may happen, but still.
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', context={'form': form})

@login_required(login_url='/users/login/')
def success_message(request):
    """Page with message after successful action"""
    username = request.user
    return render(request, 'users/success.html', context={'username': username})

@login_required(login_url='/users/login/')
def success_password_changed(request):
    """Page with message after successful changing password"""
    username = request.user
    return render(request, 'users/success_password_change.html', context={'username': username})



@login_required(login_url='/users/login/')
def acc_settings(request):
    """View for editing or changing User data.
    Later I'll change standard User model and will add some new fields (city, avatar, etc.)"""
    user = request.user
    if request.method == 'POST':
        form = AccountSettings(data=request.POST, instance=user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/users/success/')
    else:
        form = AccountSettings(instance=user)
    return render(request, 'users/acc_settings.html', context={'form': form, 'user': user})
