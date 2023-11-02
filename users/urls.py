from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from .views import register, register_success

urlpatterns = [
    path('register/', register, name='register'),
    path('success/', register_success, name='register'),
    path('login/', LoginView.as_view(template_name='users/login.html', extra_context={'next': '/edu/my/'})),
    path('logout/', LogoutView.as_view(next_page='/edu/my/')),

]
