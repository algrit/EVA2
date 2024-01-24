from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='main'),
    path('courses/', views.all_courses, name='all_courses'),  # name is used in the navbar
    path('course_sub/<int:course_id>/', views.course_sub, name='course_sub'),  # name is used in Course Sub buttons
    path('course_unsub/<int:course_id>/', views.course_unsub, name='course_unsub'),  # name is used in Course Sub buttons
    path('my_courses/', views.MyCoursesView.as_view(), name='my_courses'),  # name is used in the navbar
    path('my/<int:pk>/', views.CourseView.as_view(), name='my_course'),  # name is used my_courses.html
    path('my/<int:pk_course>/<int:pk_test>/', views.test_start, name='test_start'),  # name is used
]