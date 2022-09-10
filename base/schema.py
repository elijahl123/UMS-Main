import graphene
import graphql_jwt
from django.db.models import QuerySet
from graphql_jwt.decorators import login_required
from rest_framework_simplejwt.tokens import RefreshToken

from base.models import gen_uids
from class_calendar.types import *
from courses.types import *
from homework.types import *
from users.types import *


# noinspection PyMethodMayBeStatic
class Query(graphene.ObjectType):
    users = graphene.List(AccountType, token=graphene.String())
    user = graphene.Field(AccountType, token=graphene.String())
    calendar_events = graphene.List(CalendarEventType, token=graphene.String())
    courses = graphene.List(CourseType, token=graphene.String())
    course_times = graphene.List(CourseTimeType, token=graphene.String())
    course_files = graphene.List(CourseFileType, token=graphene.String())
    course_links = graphene.List(CourseLinkType, token=graphene.String())
    homework_assignments = graphene.List(HomeworkAssignmentType, token=graphene.String())

    @login_required
    def resolve_user(self, info, **kwargs) -> QuerySet:
        return info.context.user

    @login_required
    def resolve_users(self, info, **kwargs) -> QuerySet:
        gen_uids(Account.objects.filter(uid__isnull=True))
        return Account.objects.all() if info.context.user.is_superuser else None

    @login_required
    def resolve_calendar_events(self, info, **kwargs) -> QuerySet:
        gen_uids(CalendarEvent.objects.filter(uid__isnull=True))
        return CalendarEvent.objects.filter(course__user__uid=info.context.user.get_uid())

    @login_required
    def resolve_courses(self, info, **kwargs) -> QuerySet:
        gen_uids(Course.objects.filter(uid__isnull=True))
        return Course.objects.filter(user__uid=info.context.user.get_uid())

    @login_required
    def resolve_course_times(self, info, **kwargs) -> QuerySet:
        gen_uids(CourseTime.objects.filter(uid__isnull=True))
        return CourseTime.objects.filter(course__user__uid=info.context.user.get_uid())

    @login_required
    def resolve_course_files(self, info, **kwargs) -> QuerySet:
        gen_uids(CourseFile.objects.filter(uid__isnull=True))
        return CourseFile.objects.filter(course__user__uid=info.context.user.get_uid())

    @login_required
    def resolve_course_links(self, info, **kwargs) -> QuerySet:
        gen_uids(CourseLink.objects.filter(uid__isnull=True))
        return CourseLink.objects.filter(course__user__uid=info.context.user.get_uid())

    @login_required
    def resolve_homework_assignments(self, info, **kwargs) -> QuerySet:
        gen_uids(HomeworkAssignment.objects.filter(uid__isnull=True))
        return HomeworkAssignment.objects.filter(course__user__uid=info.context.user.get_uid())


class Mutation(graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
