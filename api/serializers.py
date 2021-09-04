from rest_framework import serializers

from courses.models import Course
from homework.models import HomeworkAssignment


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        exclude = []


class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomeworkAssignment
        exclude = []
