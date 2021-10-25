import datetime

from django import template
from pytz import timezone

from courses.models import CourseTime

register = template.Library()


@register.inclusion_tag('snippets/next_class.html', takes_context=True)
def next_class(context):
    today = datetime.datetime.now(timezone(context['account'].timezone))
    weekday = today.strftime('%A')
    coursetimes = CourseTime.objects.filter(weekday__contains=weekday, course__user=context['account']).order_by('end_time')
    next_coursetime = []
    for coursetime in coursetimes:
        end_time = timezone(context['account'].timezone).localize(datetime.datetime(today.year, today.month, today.day, coursetime.end_time.hour, coursetime.end_time.minute))
        if end_time > today:
            next_coursetime.append(coursetime)

    return {
        'coursetime': next_coursetime[0] if next_coursetime else None
    }



