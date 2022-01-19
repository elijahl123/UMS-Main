import datetime

import pytz
from django.test import TestCase

from class_calendar.models import CalendarEvent
from courses.models import *
from homework.models import *
from users.models import Account


class BaseTestCase(TestCase):
    def setUp(self) -> None:
        self.user = Account.objects.create_user(
            email='elijah.kane.1972@gmail.com',
            username='elijahl123',
            first_name='Elijah',
            last_name='Lopez',
            password='password',
        )
        self.user.timezone = 'Pacific/Honolulu'
        self.user.school = 'University of Hawaii at Manoa',
        self.user.save()
        self.course = Course.objects.create(
            name='CHEM 161',
            user=self.user,
            title='General Chemistry',
            teacher='Elijah Lopez',
            color='primary'
        )
        self.coursetime = CourseTime.objects.create(
            course=self.course,
            user=self.user,
            location='KUY 310',
            start_time='12:00:00',
            end_time='13:15:00',
            weekday="['Tuesday', 'Thursday']"
        )
        self.assignment = HomeworkAssignment.objects.create(
            name='Problems 1-10',
            course=self.course,
            due_date=datetime.date.today() + datetime.timedelta(days=3),
            due_time='23:59:00'
        )
        self.event = CalendarEvent.objects.create(
            date=datetime.date.today() + datetime.timedelta(days=2),
            user=self.user,
            time='20:00:00',
            title='Test Event'
        )
        self.now = datetime.datetime.now(tz=pytz.timezone(self.user.timezone))
        self.today = self.now.date()
        self.today_time = datetime.time(self.now.hour, self.now.minute, self.now.second)

