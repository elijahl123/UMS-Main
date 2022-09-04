from graphene_django import DjangoObjectType

from base.types import BaseType
from class_calendar.models import CalendarEvent


class CalendarEventType(BaseType):
    class Meta:
        model = CalendarEvent
        fields = (
            'uid',
            'date',
            'user',
            'time',
            'title',
            'description'
        )
