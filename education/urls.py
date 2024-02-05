from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='main'),
    path('courses/', views.all_courses, name='all_courses'),  # name is used in the navbar
    path('course_sub/<int:course_id>/', views.course_sub, name='course_sub'),  # name is used in Course Sub buttons
    path('course_unsub/<int:course_id>/', views.course_unsub, name='course_unsub'),  # name is used in Course Sub buttons
    path('my_courses/', views.MyCoursesView.as_view(), name='my_courses'),  # name is used in the navbar
    path('my/<int:pk>/', views.CourseView.as_view(), name='my_course'),  # name is used in my_courses.html, start_test_warning.html
    path('my/<int:pk_course>/<int:pk_test>/', views.start_test_warning, name='start_test_warning'),  # name is used in course_detail.html
    path('my/create_attempt/<int:pk_course>/<int:pk_test>/', views.test_att_create, name='test_att_create'),  # name is used in course_detail.html
    path('my/attempt/<int:pk_test_attempt>/', views.test_attempt, name='test_attempt'),  # name is used in view.test_att_create
    path('my/attempt/result/<int:pk_test_attempt>/', views.test_result, name='test_result'),  # name is used in view.test_attempt
]