from graphene_django import DjangoObjectType

from class_calendar.models import CalendarEvent, CalendarToken


class CalendarEventType(DjangoObjectType):
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
