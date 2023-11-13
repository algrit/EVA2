from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.urls import path

from .forms import ModalLoginForm, PwdChangeForm
from .views import register, success_message, acc_settings

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', LoginView.as_view(template_name='users/login.html', authentication_form=ModalLoginForm)),
    path('logout/', LogoutView.as_view(next_page='/edu/my/')),
    path('success/', success_message),
    path('account/', acc_settings, name='acc_settings'),
    path('password_change/',
         PasswordChangeView.as_view(template_name='users/password_change.html', form_class=PwdChangeForm,
                                    success_url='/users/success/'),
         name='password_change'),  # name is using in acc_settings.html
]
