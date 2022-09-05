from graphene_django import DjangoObjectType

from homework.models import HomeworkAssignment


class HomeworkAssignmentType(DjangoObjectType):
    class Meta:
        model = HomeworkAssignment
        fields = (
            'uid',
            'name',
            'description',
            'course',
            'due_date',
            'due_time',
            'link',
            'completed'
        )
