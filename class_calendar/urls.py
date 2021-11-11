from django.urls import path

from class_calendar.views import *

urlpatterns = [
    path('', calendar_events, name='calendar'),
    path('view/<year>/<current_month>/', calendar_events, name='calendar_custom'),
    path('add-event/', add_calendar_event, name='add_calendar_event'),
    path('delete-event/<id>/', delete_calendar_event, name='delete_calendar_event'),
    path('edit-event/<int:id>/', add_calendar_event, name='edit_calendar_event'),
    path('connect-google/', connect_google_calendar, name='connect_google_calendar'),
    path('save-google-credentials/', save_google_credentials, name='save_google_credentials'),
    path('get-google-events/', get_google_events, name='get_google_events'),
]