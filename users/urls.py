from django.contrib.auth.views import (LoginView, LogoutView, PasswordChangeView,
                                       PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView,
                                       PasswordResetCompleteView)
from django.urls import path

from .forms import ModalLoginForm, PwdChangeForm, PwdResetForm
from .views import register, acc_settings, success_signin, success_password_changed

urlpatterns = [
    path('register/', register, name='register'),
    path('success/', success_signin),
    path('login/', LoginView.as_view(template_name='users/login.html', authentication_form=ModalLoginForm)),
    path('logout/', LogoutView.as_view(next_page='/edu/my/')),
    path('account/', acc_settings, name='acc_settings'),
    path('password_change/',
         PasswordChangeView.as_view(template_name='users/password_change.html', form_class=PwdChangeForm,
                                    success_url='/users/success/password_changed/'),
         name='password_change'),  # name is using in acc_settings.html
    path('success/password_changed/', success_password_changed),

    path('password_reset/done/',
         PasswordResetDoneView.as_view(template_name='users/password_reset_done.html', extra_context={
             'title': 'Link to reset your password was sent. Check your E-mail.'}),
         name='password_reset_done'),  # name is using in PasswordResetView
    path('password_reset/', PasswordResetView.as_view(template_name='users/password_reset.html',
                                                      form_class=PwdResetForm,
                                                      subject_template_name='users/password_reset_subject.txt',
                                                      email_template_name='users/password_reset_email.html',
                                                      from_email='EVAadmin'), name='password_reset'),
    # name is using in login.html

    path('password/reset/<str:uidb64>/<str:token>/',
         PasswordResetConfirmView.as_view(template_name="users/password_reset_confirm.html"),
         name='password_reset_confirm'),  # name is using in password_reset_email.html
    path('password/reset/done/', PasswordResetCompleteView.as_view(template_name="users/password_reset_complete.html"),
         name='password_reset_complete'),

]
