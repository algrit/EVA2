from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from .forms import ModalLoginForm
from .views import register, success_message, acc_settings

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', LoginView.as_view(template_name='users/login.html', authentication_form=ModalLoginForm)),
    path('success/', success_message),
    path('logout/', LogoutView.as_view(next_page='/edu/my/')),
    path('account/', acc_settings, name='acc_settings'),
]
