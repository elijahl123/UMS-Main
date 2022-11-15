import graphene
from graphene_django.forms.mutation import DjangoModelFormMutation

from courses.forms import CourseForm, CourseTimeForm, CourseLinkForm, CourseFileForm
from courses.types import CourseType, CourseTimeType, CourseFileType, CourseLinkType


class AddCourseMutation(DjangoModelFormMutation):
    data = graphene.Field(CourseType)

    class Meta:
        form_class = CourseForm


class AddCourseTimeMutation(DjangoModelFormMutation):
    data = graphene.Field(CourseTimeType)

    class Meta:
        form_class = CourseTimeForm


class AddCourseFileMutation(DjangoModelFormMutation):
    data = graphene.Field(CourseFileType)

    class Meta:
        form_class = CourseFileForm


class AddCourseLinkMutation(DjangoModelFormMutation):
    data = graphene.Field(CourseLinkType)

    class Meta:
        form_class = CourseLinkForm
