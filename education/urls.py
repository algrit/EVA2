from django.urls import path
from . import views

urlpatterns = [
    path('my/', views.index, name='main'),
    path('courses/', views.CoursesListView.as_view()),
]