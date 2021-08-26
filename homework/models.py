import datetime

from django.db import models
# Create your models here.
from django.utils import timezone

from courses.models import Course


class HomeworkAssignment(models.Model):
    name = models.CharField(max_length=120, null=True)
    description = models.TextField(null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)
    due_date = models.DateField(null=True)
    due_time = models.TimeField(default='09:00:00')
    link = models.URLField(null=True, blank=True)
    completed = models.BooleanField(default=False)
