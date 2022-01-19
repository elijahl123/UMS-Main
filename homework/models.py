import datetime
from typing import Union

import numpy as np
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import QuerySet
from pytz import timezone

from courses.models import Course
from users.models import Account


class HomeworkManager(models.Manager):
    def late_assignments(self, user: Account, **kwargs: dict) -> QuerySet:
        late_assignments = []
        for assignment in self.filter(course__user=user, completed=False, **kwargs):
            if timezone(user.timezone).localize(assignment.due_datetime) < datetime.datetime.now(
                    timezone(user.timezone)):
                late_assignments.append(assignment)
        return HomeworkAssignment.objects.filter(id__in=list(map(lambda x: x.id, late_assignments)))

    def all_assignments(self, user: Account, reading: bool = False, **kwargs: dict) -> QuerySet:
        all_assignments = []
        for assignment in self.filter(course__user=user, completed=False, **kwargs):
            if timezone(user.timezone).localize(assignment.due_datetime) >= datetime.datetime.now(
                    timezone(user.timezone)):
                all_assignments.append(assignment)
        model: Union[HomeworkAssignment, ReadingAssignment] = ReadingAssignment if reading else HomeworkAssignment
        return model.objects.filter(id__in=list(map(lambda x: x.id, all_assignments)))

    def upcoming_assignments(self, user: Account, days: int = 2, **kwargs: dict) -> QuerySet:
        upcoming_assignments = []
        date_delta = datetime.datetime.now(timezone(user.timezone)) + datetime.timedelta(days=days)
        for assignment in self.all_assignments(user, **kwargs):
            if timezone(user.timezone).localize(assignment.due_datetime) <= date_delta:
                upcoming_assignments.append(assignment)
        return HomeworkAssignment.objects.filter(id__in=list(map(lambda x: x.id, upcoming_assignments)))

    def date_range(self, user: Account, **kwargs: dict) -> set:
        used_dates = []

        for assignment in self.all_assignments(user, **kwargs):
            used_dates.append(assignment.due_date)
        for reading, reading_date, start_page, end_page in ReadingAssignment.get_recommended_readings(user):
            if start_page and end_page:
                used_dates.append(reading_date)

        return set(used_dates)


class HomeworkAssignment(models.Model):
    objects = HomeworkManager()

    name = models.CharField(max_length=120, null=True)
    description = models.TextField(null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)
    due_date = models.DateField(null=True)
    due_time = models.TimeField(default='23:59:00')
    link = models.URLField(null=True, blank=True)
    completed = models.BooleanField(default=False)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super().save(force_insert, force_update, using, update_fields)

    @property
    def due_datetime(self):
        return datetime.datetime(self.due_date.year, self.due_date.month, self.due_date.day, self.due_time.hour,
                                 self.due_time.minute, self.due_time.second)

    def is_reading(self):
        return ReadingAssignment.objects.filter(homeworkassignment_ptr_id=self.id).exists()

    class Meta:
        ordering = ['due_date', 'due_time', 'course']

    def __str__(self):
        return self.name


class ReadingAssignment(HomeworkAssignment):
    modified = models.DateField(auto_now=True)
    start_page = models.IntegerField(null=True)
    end_page = models.IntegerField(null=True)
    include_due_date = models.BooleanField(
        default=False,
        verbose_name='Include Due Date in Reading Plan',
        help_text='Check this if you want the daily readings to end on the due date or on the day before.'
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['due_date', 'due_time', 'course']

    @staticmethod
    def get_recommended_readings(user: Account) -> tuple:

        out_list = []

        reading: ReadingAssignment
        for reading in ReadingAssignment.objects.filter(course__user=user, completed=False):

            uploaded: datetime.date = datetime.date(reading.modified.year, reading.modified.month, reading.modified.day)
            due: datetime.date = datetime.date(reading.due_date.year, reading.due_date.month, reading.due_date.day)
            delta: int = (due - uploaded).days + 1
            if reading.include_due_date:
                delta += 1

            if delta > reading.end_page - (reading.start_page - 1):
                delta = reading.end_page - reading.start_page + 2

            daily_pages = list(map(lambda x: round(x), np.linspace(reading.start_page - 1, reading.end_page, delta)))

            for val in range(delta - 1):
                out_list.append(
                    (reading, uploaded + datetime.timedelta(days=val), daily_pages[val] + 1, daily_pages[val + 1]))

        return out_list
