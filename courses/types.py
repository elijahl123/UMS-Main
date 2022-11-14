import graphene
from graphene_django import DjangoObjectType

from courses.models import *


class CourseType(DjangoObjectType):
    class Meta:
        model = Course
        fields = [
            'uid',
            'name',
            'user',
            'title',
            'teacher',
            'color'
        ]
        filter_fields = [
            'uid',
            'name',
            'user',
            'title',
            'teacher',
            'color'
        ]
        interfaces = (graphene.relay.Node,)


class CourseTimeType(DjangoObjectType):
    class Meta:
        model = CourseTime
        fields = [
            'uid',
            'course',
            'user',
            'location',
            'start_time',
            'end_time',
            'weekday',
            'link',
            'zoom_password'
        ]
        filter_fields = [
            'uid',
            'course__uid',
            'user',
            'location',
            'start_time',
            'end_time',
            'weekday',
            'link',
            'zoom_password'
        ]
        interfaces = (graphene.relay.Node,)


class CourseFileType(DjangoObjectType):
    class Meta:
        model = CourseFile
        fields = [
            'uid',
            'course',
            'title',
        ]
        filter_fields = [
            'uid',
            'course__uid',
            'title',
        ]
        interfaces = (graphene.relay.Node,)


class CourseLinkType(DjangoObjectType):
    class Meta:
        model = CourseLink
        fields = [
            'uid',
            'course',
            'title',
            'link',
        ]
        filter_fields = [
            'uid',
            'course__uid',
            'title',
            'link',
        ]
        interfaces = (graphene.relay.Node,)
