import datetime

from django import template
from django.core.exceptions import ObjectDoesNotExist

from courses.models import CourseTime, Course
from notes.models import Note

register = template.Library()


@register.simple_tag
def num_notes(course):
    try:
        obj = Course.objects.get(id=course)
    except ObjectDoesNotExist:
        obj = None

    return Note.objects.filter(course=obj).count() if obj else '0'
