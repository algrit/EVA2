from django.urls import path
from . import views

urlpatterns = [
    path('my/', views.index, name='main'),
    path('courses/', views.subscribe, name='all_courses'),  # name is used in the navbar
]