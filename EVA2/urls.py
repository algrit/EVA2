from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('edu/', include('education.urls')),
    path('users/', include('users.urls')),
]
