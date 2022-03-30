import datetime
from dataclasses import dataclass
from typing import Union, Type, List

import numpy as np
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import QuerySet
from pytz import timezone

from base.models import ReminderMixin
from courses.models import Course
from users.models import Account


class ReadingDay:
    reading = None
    date: datetime.date
    start_page: int
    end_page: int

    def __init__(self, reading, date: datetime.date, start_page: int, end_page: int):
        self.reading = reading
        self.date = date
        self.start_page = start_page
        self.end_page = end_page

    def __repr__(self):
        return f"ReadingDay(reading={self.reading}, date={self.date}, start_page={self.start_page}, end_page={self.end_page})"


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
        model: Type[Union[HomeworkAssignment, ReadingAssignment]] = ReadingAssignment if reading else HomeworkAssignment
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

        for day in ReadingAssignment.get_recommended_readings(user):
            if day.start_page and day.end_page:
                used_dates.append(day.date)

        return set(used_dates)


class HomeworkAssignment(ReminderMixin):
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
    def get_recommended_readings(user: Account) -> ReadingDay:

        out_list: List[ReadingDay] = []

        reading: ReadingAssignment
        for reading in ReadingAssignment.objects.filter(course__user=user, completed=False):

            uploaded: datetime.date = datetime.date(reading.modified.year, reading.modified.month, reading.modified.day)
            due: datetime.date = datetime.date(reading.due_date.year, reading.due_date.month, reading.due_date.day)
            delta: int = (due - uploaded).days + 1
            if reading.include_due_date:
                delta += 1

            if delta < 0:
                return []

            if delta > reading.end_page - (reading.start_page - 1):
                delta = reading.end_page - reading.start_page + 2

            daily_pages = list(map(lambda x: round(x), np.linspace(reading.start_page - 1, reading.end_page, delta)))

            for val in range(delta - 1):
                reading_day = ReadingDay(reading, uploaded + datetime.timedelta(days=val), daily_pages[val] + 1, daily_pages[val + 1])
                out_list.append(reading_day)

        return out_list
