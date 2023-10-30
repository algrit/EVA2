from django.http import HttpResponseRedirect
from django.shortcuts import render

from .forms import UserRegisterForm


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/edu/index/')
        else:
            return render(request, 'registration/register.html', context={'form': form})
    else:
        form = UserRegisterForm()
    return render(request, 'registration/register.html', context={'form': form})


def add_info(request):
    return render(request, 'registration/add_info.html')
