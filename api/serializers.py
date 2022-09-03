from abc import ABC

from django.forms import model_to_dict
from rest_framework import serializers

from courses.models import Course, CourseTime
from homework.models import HomeworkAssignment


