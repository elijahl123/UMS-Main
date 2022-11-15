import graphene
from graphene_django.forms.mutation import DjangoModelFormMutation

from courses.forms import CourseForm, CourseTimeForm, CourseLinkForm, CourseFileForm
from homework.forms import HomeworkAssignmentForm
from homework.types import HomeworkAssignmentType


class AddHomeworkAssignmentMutation(DjangoModelFormMutation):
    data = graphene.Field(HomeworkAssignmentType)

    class Meta:
        form_class = HomeworkAssignmentForm
