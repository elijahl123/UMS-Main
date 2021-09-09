import calendar
import json
from datetime import date

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

# Create your views here.
from class_calendar.forms import AddEvent
from class_calendar.models import CalendarEvent, CalendarToken
from courses.models import CourseTime
from homework.models import HomeworkAssignment
from school.models import School

context = {'schools': School.objects.all()}


@login_required
def add_calendar_event(request, id=0):
    context['account'] = request.user

    context['form_title'] = 'Add Calendar Event'
    context['form_description'] = 'Here, you can add an event to the calendar and not forget any important dates'
    context['excluded_fields'] = ['user']

    event_instance = None

    if id:
        event_instance = get_object_or_404(CalendarEvent, id=id)
        if not event_instance.user == request.user:
            return redirect('calendar')
        context['form_title'] = 'Edit Calendar Event'

    if request.POST:
        form = AddEvent(request.POST, instance=event_instance if id else None)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            messages.success(request, 'New Event Added')
            return redirect('calendar')
    else:
        form = AddEvent(instance=event_instance if id else None, initial={'date': request.GET.get('date')})

    context['form'] = form

    return render(request, 'forms/add_event.html', context)


@login_required
def calendar_events(request, year=None, current_month=None):
    context['account'] = request.user
    c = calendar.Calendar(6)
    todays_date = date.today()

    context['today'] = todays_date

    if (current_month and int(current_month) > 12) or todays_date.month > 12:
        return redirect('calendar_custom', int(year) + 1, 1)
    if (current_month and int(current_month) < 1) or todays_date.month < 1:
        return redirect('calendar_custom', int(year) - 1, 12)

    if year and current_month:
        context['previous_month'] = int(current_month) - 1
        context['previous_year'] = year
        context['next_month'] = int(current_month) + 1
        context['next_year'] = year
    else:
        context['previous_month'] = todays_date.month - 1
        context['previous_year'] = todays_date.year
        context['next_month'] = todays_date.month + 1
        context['next_year'] = todays_date.year

    context['this_month'] = calendar.month_name[int(current_month) if current_month else todays_date.month]
    context['this_year'] = year or todays_date.year

    context['coursetimes'] = CourseTime.objects.filter(user=request.user)
    context['days'] = c.monthdatescalendar(
        int(year if year else todays_date.year),
        int(current_month if current_month else todays_date.month)
    )
    context['homework_assignments'] = HomeworkAssignment.objects.filter(completed=False, course__user=request.user)

    context['calendar_events'] = CalendarEvent.objects.filter(user=request.user)

    return render(request, 'calendar.html', context)


@login_required
def delete_calendar_event(request, id):
    context['account'] = request.user
    event = get_object_or_404(CalendarEvent, id=id)
    event.delete()
    return redirect('calendar')


@login_required
def connect_google_calendar(request):
    context['account'] = request.user

    SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if CalendarToken.objects.filter(user=request.user).exists():
        creds = Credentials.from_authorized_user_info(json.loads(CalendarToken.objects.get(user=request.user).token),
                                                      SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            credentials = {"web": {
                "client_id": "9730399367-hikc9cjjco8kpn750po400dmo4ke3uhu.apps.googleusercontent.com",
                "project_id": "untitled-management-software",
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                "client_secret": "OunQv9kY3lmfXdaRGBOuo6JH",
                "redirect_uris": ["http://localhost/accounts/google/login/callback/",
                                  "https://client.untitledmanagementsoftware.com/accounts/google/login/callback/",
                                  "http://localhost/calendar/connect-google/",
                                  "https://client.untitledmanagementsoftware.com/calendar/connect-google/",
                                  "http://localhost/",
                                  "http://client.untitledmanagementsoftware.com/"]
            }
            }
            flow = InstalledAppFlow.from_client_config(
                credentials, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        CalendarToken.objects.update_or_create(user=request.user, token=creds.to_json())

    return redirect('calendar')
