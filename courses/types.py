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


class CourseFileType(DjangoObjectType):
    class Meta:
        model = CourseTime
        fields = [
            'uid',
            'course',
            'title',
            'file',
            'uploaded'
        ]


class CourseLinkType(DjangoObjectType):
    class Meta:
        model = CourseTime
        fields = [
            'uid',
            'course',
            'title',
            'link',
            'uploaded',
        ]
