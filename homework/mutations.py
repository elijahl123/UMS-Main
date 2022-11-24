import graphene
from graphene_django.forms.mutation import DjangoModelFormMutation, _set_errors_flag_to_context
from graphene_django.types import ErrorType

from courses.forms import CourseForm, CourseTimeForm, CourseLinkForm, CourseFileForm
from courses.models import Course
from homework.forms import HomeworkAssignmentForm
from homework.types import HomeworkAssignmentType


class AddHomeworkAssignmentMutation(DjangoModelFormMutation):
    data = graphene.Field(HomeworkAssignmentType)

    class Meta:
        form_class = HomeworkAssignmentForm


