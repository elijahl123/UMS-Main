import graphene
from graphene_django.forms.mutation import DjangoModelFormMutation

from class_calendar.forms import AddEvent
from class_calendar.types import CalendarEventType


class AddEventMutation(DjangoModelFormMutation):
    data = graphene.Field(CalendarEventType)

    class Meta:
        form_class = AddEvent
