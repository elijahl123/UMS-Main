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

from class_calendar.views import calendar_events, add_calendar_event, delete_calendar_event
from courses.views import *
from homework.views import homework, add_assignment, delete_assignment, complete_assignment
from users.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', index, name='index'),
    path('account/', account, name='account'),
    path('account/settings/', account_settings, name='account_settings'),
    path('account/settings/change-account-calendar-view/', change_account_calendar_view,
         name='change_account_calendar_view'),
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
    path('calendar/', calendar_events, name='calendar'),
    path('calendar/view/<year>/<current_month>/', calendar_events, name='calendar_custom'),
    path('calendar/add-event/', add_calendar_event, name='add_calendar_event'),
    path('calendar/delete-event/<id>/', delete_calendar_event, name='delete_calendar_event'),
    path('calendar/edit-event/<int:id>/', add_calendar_event, name='edit_calendar_event'),
    path('homework/', homework, name='homework'),
    path('homework/add-assignment/', add_assignment, name='add_assignment'),
    path('homework/edit-assignment/<id>/', add_assignment, name='edit_assignment'),
    path('homework/delete-assignment/<id>/', delete_assignment, name='delete_assignment'),
    path('homework/complete-assignment/<id>/', complete_assignment, name='complete_assignment')
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
