import graphene
from django.db.models import QuerySet

from class_calendar.models import CalendarEvent
from class_calendar.types import CalendarEventType


class CalendarEventQuery(graphene.ObjectType):
    all_calendar_events = graphene.List(CalendarEventType)

    def resolve(self, info, user_uid, **kwargs) -> QuerySet:
        return CalendarEvent.objects.filter(user__uid=user_uid)


# class CalendarEventMutation(graphene.Mutation):
#     class Arguments:
#         pass
#
#     def mutate(self, info) -> graphene.Mutation:
#         pass


schema = graphene.Schema(query=CalendarEventQuery)
