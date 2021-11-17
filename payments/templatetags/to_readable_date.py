import datetime

from django import template
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse

from courses.models import CourseTime, Course
from notes.models import Note

register = template.Library()


@register.filter
def to_readable_date(value):
    if isinstance(value, int):
        date = datetime.datetime.fromtimestamp(value)
    else:
        date = None
    return date
