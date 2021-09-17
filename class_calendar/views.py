import calendar
import datetime
import json
from datetime import date

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
# Create your views here.
from googleapiclient.discovery import build

from UMSMain.settings import GOOGLE_API_CREDENTIALS, GOOGLE_API_SCOPES
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

    creds = CalendarToken.objects.get_credentials(request.user)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = Flow.from_client_config(
                GOOGLE_API_CREDENTIALS, GOOGLE_API_SCOPES)
            flow.redirect_uri = request.build_absolute_uri(reverse('save_google_credentials'))
            authorization_url, state = flow.authorization_url(
                # Enable offline access so that you can refresh an access token without
                # re-prompting the user for permission. Recommended for web server apps.
                access_type='offline',
                login_hint=request.user.email,
                # Enable incremental authorization. Recommended as a best practice.
                include_granted_scopes='true')
            # Save the credentials for the next run
            return HttpResponseRedirect(authorization_url)

    return redirect('calendar')


@login_required
def save_google_credentials(request):
    flow = Flow.from_client_config(
        GOOGLE_API_CREDENTIALS, scopes=None, state=request.GET.get('state'))

    flow.redirect_uri = request.build_absolute_uri(reverse('save_google_credentials'))

    flow.fetch_token(code=request.GET.get('code'))
    token_credentials = flow.credentials
    token = {
        'token': token_credentials.token,
        'refresh_token': token_credentials.refresh_token,
        'token_uri': token_credentials.token_uri,
        'client_id': token_credentials.client_id,
        'client_secret': token_credentials.client_secret,
        'scopes': token_credentials.scopes
    }

    obj, obj_exists = CalendarToken.objects.get_or_create(user=request.user)
    obj.token = json.dumps(token)
    obj.save()
    return redirect('calendar')


@login_required
def get_google_events(request):
    context['account'] = request.user

    creds = Credentials(**CalendarToken.objects.get_token(request.user))
    if not creds:
        return redirect('connect_google_calendar')

    service = build('calendar', 'v3', credentials=creds)

    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    print('Getting the upcoming 10 events')
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                          maxResults=10, singleEvents=True,
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])
