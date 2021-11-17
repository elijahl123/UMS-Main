import datetime

from django import template
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse

from courses.models import CourseTime, Course
from notes.models import Note

register = template.Library()


@register.filter
def divide(value, arg):
    try:
        return int(value) / int(arg)
    except (ValueError, ZeroDivisionError):
        return None
