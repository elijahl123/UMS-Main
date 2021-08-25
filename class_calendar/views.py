import calendar
from datetime import date

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

# Create your views here.
from courses.models import CourseTime
from school.models import School

context = {'schools': School.objects.all()}


@login_required
def calendar_events(request, year=None, current_month=None):
    context['account'] = request.user
    c = calendar.Calendar(6)
    todays_date = date.today()

    if int(current_month) > 12 or todays_date.month > 12:
        return redirect('calendar_custom', int(year) + 1, 1)
    if int(current_month) < 1 or todays_date.month < 1:
        return redirect('calendar_custom', int(year) - 1, 12)

    if year and current_month:
        context['previous_month'] = int(current_month) - 1
        context['previous_year'] = year
        context['next_month'] = int(current_month) + 1
        context['next_year'] = year
    else:
        context['previous_month'] = todays_date.month - 1
        context['previous_year'] = todays_date.year
        context['next_month'] = todays_date.month
        context['next_year'] = todays_date.year

    context['this_month'] = calendar.month_name[int(current_month) if current_month else todays_date.month]
    context['this_year'] = year or todays_date.year

    context['coursetimes'] = CourseTime.objects.filter(user=request.user)
    context['days'] = c.monthdatescalendar(
        int(year if year else todays_date.year),
        int(current_month if current_month else todays_date.month)
    )

    return render(request, 'calendar.html', context)
