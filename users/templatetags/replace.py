import datetime

from django import template
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse

from courses.models import CourseTime, Course
from notes.models import Note

register = template.Library()


@register.filter(name='replace')
def replace(value, args):

    values = args.split(',')

    return value.replace(*values)
