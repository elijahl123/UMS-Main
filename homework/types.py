import graphene
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
            'completed',
            'alert',
            'second_alert'
        )
        filter_fields = [
            'uid',
            'name',
            'description',
            'course__uid',
            'due_date',
            'due_time',
            'link',
            'completed',
            'alert',
            'second_alert'
        ]
        interfaces = (graphene.relay.Node,)
