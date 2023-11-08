from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render

from .forms import UserRegisterForm, AccountSettings


def register(request):
    """It's a common view function, but I decided to add low-level authenticate just after registration"""
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
                return HttpResponse('SOMETHING WRONG IN USER AUTH')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', context={'form': form})


def register_success(request):
    username = request.user
    return render(request, 'users/success.html', context={'username': username})


def acc_settings(request, id_user):
    user = User.objects.get(id=id_user)
    if request.method == 'POST':
        form = AccountSettings(data=request.POST, instance=user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/users/success/')
    else:
        form = AccountSettings(instance=user)
    return render(request, 'users/acc_settings.html', context={'form': form, 'user': user})