"""UMSMain URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from courses.views import *
from homework.views import *
from school.views import add_school
from users.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('privacy-policy/', privacy_policy, name='privacy_policy'),
    path('api-auth/', include('rest_framework.urls')),
    path('api/', include('api.urls')),
    path('', index, name='index'),
    path('feedback/', feedback, name='feedback'),
    path('account/', include('users.urls')),
    path('class-schedule/', class_schedule, name='class_schedule'),
    path('manage-schedule/', manage_schedule, name='manage_schedule'),
    path('add-coursetime/', add_coursetime, name='add_coursetime'),
    path('edit-coursetime/<id>/', edit_coursetime, name='edit_coursetime'),
    path('delete-coursetime/<id>/', delete_coursetime, name='delete_coursetime'),
    path('add-course/', add_course, name='add_course'),
    path('delete-course/<id>/', delete_course, name='delete_course'),
    path('edit-course/<id>/', edit_course, name='edit_course'),
    path('courses/', include('courses.course_urls')),
    path('add-school/', add_school, name='add_school'),
    path('add-timezone/', select_timezone, name='select_timezone'),
    path('calendar/', include('class_calendar.urls')),
    path('homework/', include('homework.urls')),
    path('notes/', include('notes.urls')),
    path('payments/', include('payments.urls'))
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
