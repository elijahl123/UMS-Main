from django.urls import path

from users.views import *

urlpatterns = [
    path('', account, name='account'),
    path('settings/', account_settings, name='account_settings'),
    path('settings/change-account-calendar-view/', change_account_calendar_view,
         name='change_account_calendar_view'),
]