import graphene
from django.db.models import QuerySet

from base.models import gen_uids
from class_calendar.types import *
from courses.types import *
from homework.types import *
from users.types import *


# noinspection PyMethodMayBeStatic
class Query(graphene.ObjectType):
    users = graphene.List(AccountType)
    user = graphene.Field(AccountType)
    calendar_events = graphene.List(CalendarEventType)
    courses = graphene.List(CourseType)
    course_times = graphene.List(CourseTimeType)
    course_files = graphene.List(CourseFileType)
    course_links = graphene.List(CourseLinkType)
    homework_assignments = graphene.List(HomeworkAssignmentType)

    def resolve_user(self, info, **kwargs) -> QuerySet:
        return Account.objects.get(uid=info.context.user.get_uid()) if info.context.user.is_superuser else None

    def resolve_users(self, info, **kwargs) -> QuerySet:
        gen_uids(Account.objects.filter(uid__isnull=True))
        return Account.objects.all() if info.context.user.is_superuser else None

    def resolve_calendar_events(self, info, **kwargs) -> QuerySet:
        gen_uids(CalendarEvent.objects.filter(uid__isnull=True))
        return CalendarEvent.objects.filter(course__user__uid=info.context.user.get_uid())

    def resolve_courses(self, info, **kwargs) -> QuerySet:
        gen_uids(Course.objects.filter(uid__isnull=True))
        return Course.objects.filter(user__uid=info.context.user.get_uid())

    def resolve_course_times(self, info, **kwargs) -> QuerySet:
        gen_uids(CourseTime.objects.filter(uid__isnull=True))
        return CourseTime.objects.filter(course__user__uid=info.context.user.get_uid())

    def resolve_course_files(self, info, **kwargs) -> QuerySet:
        gen_uids(CourseFile.objects.filter(uid__isnull=True))
        return CourseFile.objects.filter(course__user__uid=info.context.user.get_uid())

    def resolve_course_links(self, info, **kwargs) -> QuerySet:
        gen_uids(CourseLink.objects.filter(uid__isnull=True))
        return CourseLink.objects.filter(course__user__uid=info.context.user.get_uid())

    def resolve_homework_assignments(self, info, **kwargs) -> QuerySet:
        gen_uids(HomeworkAssignment.objects.filter(uid__isnull=True))
        return HomeworkAssignment.objects.filter(course__user__uid=info.context.user.get_uid())


# class Mutation(graphene.Mutation):
#     class Arguments:
#         pass
#
#     def mutate(self, info) -> graphene.Mutation:
#         pass


schema = graphene.Schema(query=Query)
