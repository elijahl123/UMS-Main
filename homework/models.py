import datetime
import math

from django.db import models

from courses.models import Course


# Create your models here.


class HomeworkAssignment(models.Model):
    name = models.CharField(max_length=120, null=True)
    description = models.TextField(null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)
    due_date = models.DateField(null=True)
    due_time = models.TimeField(default='23:59:00')
    link = models.URLField(null=True, blank=True)
    completed = models.BooleanField(default=False)

    def is_reading(self):
        return ReadingAssignment.objects.filter(homeworkassignment_ptr_id=self.id).exists()

    class Meta:
        ordering = ['due_date', 'due_time']


class ReadingAssignment(HomeworkAssignment):
    uploaded = models.DateField(auto_now=True)
    start_page = models.IntegerField(null=True)
    end_page = models.IntegerField(null=True)

    @classmethod
    def get_recommended_readings(cls, user):

        out_list = []

        for reading in cls.objects.filter(course__user=user, completed=False):

            uploaded = datetime.date(reading.uploaded.year, reading.uploaded.month, reading.uploaded.day)
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
                out_list.append((reading, uploaded + datetime.timedelta(days=i), get_pages('start', i), get_pages('end', i)))

        return out_list
