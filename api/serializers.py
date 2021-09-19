from abc import ABC

from django.forms import model_to_dict
from rest_framework import serializers

from courses.models import Course, CourseTime
from homework.models import HomeworkAssignment


class CourseRelatedField(serializers.RelatedField):
    def to_representation(self, instance):
        return model_to_dict(instance)


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        exclude = []


class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomeworkAssignment
        exclude = []


class CoursetimeSerializer(serializers.ModelSerializer):
    course = CourseRelatedField(read_only=True)

    class Meta:
        model = CourseTime
        exclude = []
