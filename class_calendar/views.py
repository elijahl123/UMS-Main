import calendar
from datetime import date

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from class_calendar.forms import AddEvent
from class_calendar.models import CalendarEvent
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
        form = AddEvent(instance=event_instance if id else None)

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
    context['homework_assignments'] = HomeworkAssignment.objects.filter(completed=False)

    context['calendar_events'] = CalendarEvent.objects.filter(user=request.user)

    return render(request, 'calendar.html', context)

@login_required
def delete_calendar_event(request, id):
    context['account'] = request.user
    event = get_object_or_404(CalendarEvent, id=id)
    event.delete()
    return redirect('calendar')