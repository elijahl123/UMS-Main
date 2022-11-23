import graphene
import graphql_jwt
from django.db.models import QuerySet
from graphene_django.filter import DjangoFilterConnectionField
from graphql_jwt.decorators import login_required
from rest_framework_simplejwt.tokens import RefreshToken

from base.models import gen_uids
from class_calendar.mutations import AddCalendarEventMutation
from class_calendar.types import *
from courses.mutations import AddCourseMutation, AddCourseTimeMutation, AddCourseFileMutation, AddCourseLinkMutation
from courses.types import *
from homework.mutations import AddHomeworkAssignmentMutation
from homework.types import *
from notes.models import Note
from notes.types import NoteType
from users.mutations import SignupMutation, AddEmailMutation, ChangePasswordMutation, SetPasswordMutation, \
    ResetPasswordMutation, ResetPasswordKeyMutation
from users.types import *


# noinspection PyMethodMayBeStatic
class Query(graphene.ObjectType):
    users = DjangoFilterConnectionField(AccountType, token=graphene.String())
    user = graphene.Field(AccountType, token=graphene.String())
    calendar_events = DjangoFilterConnectionField(CalendarEventType, token=graphene.String())
    courses = DjangoFilterConnectionField(CourseType, token=graphene.String())
    course_times = DjangoFilterConnectionField(CourseTimeType, token=graphene.String())
    course_files = DjangoFilterConnectionField(CourseFileType, token=graphene.String())
    course_links = DjangoFilterConnectionField(CourseLinkType, token=graphene.String())
    homework_assignments = DjangoFilterConnectionField(HomeworkAssignmentType, token=graphene.String())
    notes = DjangoFilterConnectionField(NoteType, token=graphene.String())

    get_schedule = graphene.List(CourseTimeType, token=graphene.String(), date=graphene.Date())

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
        return CalendarEvent.objects.filter(user__uid=info.context.user.get_uid())

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

    @login_required
    def resolve_notes(self, info, **kwargs) -> QuerySet:
        gen_uids(Note.objects.filter(uid__isnull=True))
        return Note.objects.filter(course__user__uid=info.context.user.get_uid())

    @login_required
    def resolve_get_schedule(self, info, **kwargs) -> QuerySet:
        # Get the day of the week from the date in string format
        day = kwargs.get('date').strftime('%A')
        # Get the course times for the day
        course_times = CourseTime.objects.filter(course__user__uid=info.context.user.get_uid(), weekday__icontains=day)
        return course_times


class Mutation(graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()

    signup = SignupMutation.Field()
    add_email = AddEmailMutation.Field()
    change_password = ChangePasswordMutation.Field()
    set_password = SetPasswordMutation.Field()
    reset_password = ResetPasswordMutation.Field()
    reset_password_key = ResetPasswordKeyMutation.Field()

    add_calendar_event = AddCalendarEventMutation.Field()
    add_course = AddCourseMutation.Field()
    add_course_time = AddCourseTimeMutation.Field()
    add_course_file = AddCourseFileMutation.Field()
    add_course_link = AddCourseLinkMutation.Field()
    add_homework_assignment = AddHomeworkAssignmentMutation.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
