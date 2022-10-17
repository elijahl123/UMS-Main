import graphene
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
        filter_fields = [
            'uid',
            'date',
            'user',
            'time',
            'title',
            'description'
        ]
        interfaces = (graphene.relay.Node,)
