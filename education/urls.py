from django.urls import path
from . import views


urlpatterns = [
    path('my/', views.index, name='main'),
    path('courses/', views.all_courses, name='all_courses'),  # name is used in the navbar
    path('course_sub/<int:course_id>/', views.course_sub, name='course_sub'),
]