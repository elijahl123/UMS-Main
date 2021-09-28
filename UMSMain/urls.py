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
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.decorators.cache import cache_control
from django.views.generic import TemplateView

from class_calendar.views import calendar_events, add_calendar_event, delete_calendar_event, connect_google_calendar, \
    save_google_credentials, get_google_events
from courses.views import *
from homework.views import homework, add_assignment, delete_assignment, complete_assignment, add_reading_assignment, \
    delete_reading_assignment
from school.views import add_school
from users.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('privacy-policy/', privacy_policy, name='privacy_policy'),
    path('api-auth/', include('rest_framework.urls')),
    path('api/', include('api.urls')),
    url(r'^sw.js', cache_control(max_age=2592000)(TemplateView.as_view(
        template_name="sw.js",
        content_type='application/javascript',
    )), name='sw.js'),
    url(r'^manifest.json', cache_control(max_age=2592000)(TemplateView.as_view(
        template_name="manifest.json",
        content_type='application/json',
    )), name='manifest.json'),
    path('', index, name='index'),
    path('feedback/', feedback, name='feedback'),
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
    path('calendar/connect-google/', connect_google_calendar, name='connect_google_calendar'),
    path('calendar/save-google-credentials/', save_google_credentials, name='save_google_credentials'),
    path('calendar/get-google-events/', get_google_events, name='get_google_events'),
    path('homework/', homework, name='homework'),
    path('homework/add-assignment/', add_assignment, name='add_assignment'),
    path('homework/edit-assignment/<id>/', add_assignment, name='edit_assignment'),
    path('homework/delete-assignment/<id>/', delete_assignment, name='delete_assignment'),
    path('homework/add-reading-assignment/', add_reading_assignment, name='add_reading_assignment'),
    path('homework/edit-reading-assignment/<id>/', add_reading_assignment, name='edit_reading_assignment'),
    path('homework/delete-reading-assignment/<id>/', delete_reading_assignment, name='delete_reading_assignment'),
    path('homework/complete-assignment/<id>/', complete_assignment, name='complete_assignment')
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
