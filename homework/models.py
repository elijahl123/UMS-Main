import datetime
import math

from django.db import models

from courses.models import Course


# Create your models here.

class HomeworkManager(models.Manager):
    def late_assignments(self, user):
        late_assignments = []
        for assignment in self.filter(course__user=user, completed=False):
            if assignment.due_datetime < datetime.datetime.now():
                late_assignments.append(assignment)
        return late_assignments

    def all_assignments(self, user):
        all_assignments = []
        for assignment in self.filter(course__user=user, completed=False):
            if assignment.due_datetime >= datetime.datetime.now():
                all_assignments.append(assignment)
        return all_assignments

    def upcoming_assignments(self, user):
        upcoming_assignments = []
        tomorrow = datetime.datetime.today() + datetime.timedelta(days=2)
        for assignment in self.all_assignments(user):
            if assignment.due_datetime <= tomorrow:
                upcoming_assignments.append(assignment)
        return upcoming_assignments

    def date_range(self, user):
        used_dates = []

        for assignment in self.all_assignments(user):
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

    @property
    def due_datetime(self):
        return datetime.datetime(self.due_date.year, self.due_date.month, self.due_date.day, self.due_time.hour,
                                 self.due_time.minute, self.due_time.second)

    def is_reading(self):
        return ReadingAssignment.objects.filter(homeworkassignment_ptr_id=self.id).exists()

    class Meta:
        ordering = ['due_date', 'due_time']

    def __str__(self):
        return self.name


class ReadingAssignment(HomeworkAssignment):
    modified = models.DateField(auto_now=True)
    start_page = models.IntegerField(null=True)
    end_page = models.IntegerField(null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['course']

    @classmethod
    def get_recommended_readings(cls, user):

        out_list = []

        for reading in cls.objects.filter(course__user=user, completed=False):

            uploaded = datetime.date(reading.modified.year, reading.modified.month, reading.modified.day)
            due = datetime.date(reading.due_date.year, reading.due_date.month, reading.due_date.day)
            delta = (due - uploaded).days

            def get_pages(scope, index):
                daily_pages = math.ceil((reading.end_page - reading.start_page) / delta)

                start_page = reading.start_page + (daily_pages * index)
                end_page = reading.start_page + (daily_pages * (index + 1))

                if start_page > reading.end_page:
                    return 0

                if end_page > reading.end_page:
                    return start_page if scope == 'start' else reading.end_page

                return start_page if scope == 'start' else end_page

            for i in range(delta):
                out_list.append(
                        (reading, uploaded + datetime.timedelta(days=i), get_pages('start', i), get_pages('end', i)))

        return out_list
