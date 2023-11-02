from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from .views import register

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', LoginView.as_view(template_name='registration/login.html', extra_context={'next': '/edu/my/'})),
    path('logout/', LogoutView.as_view(next_page='/users/login/'), name='logout'),

]
