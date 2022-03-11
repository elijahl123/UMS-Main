import datetime

import pytz
from django.test import TestCase, Client
from django.urls import reverse

from class_calendar.models import CalendarEvent
from courses.models import *
from homework.models import *
from users.models import Account


class BaseTestCase(TestCase):
    def setUp(self) -> None:
        # ############################################## User Creation #################################################

        self.user = Account.objects.create_user(
            email='elijah.kane.1972@gmail.com',
            username='elijahl123',
            first_name='Elijah',
            last_name='Lopez',
            password='password',
        )
        self.user.timezone = 'Pacific/Honolulu'
        self.user.school = 'University of Hawaii at Manoa'
        self.user.exempt_from_payment = True
        self.user.save()

        # ############################################### Client Login #################################################

        self.client = Client()
        logged_in = self.client.login(email=self.user.email, password="password")
        self.assertTrue(logged_in)
        response = self.client.get(reverse("index"))
        self.assertTrue(response.status_code == 200)

        # ############################################## User 2 Creation ###############################################

        self.user2 = Account.objects.create_user(
            email='elijah.lopez.1972@gmail.com',
            username='elijahl95',
            first_name='Jude',
            last_name='Lopez',
            password='password1',
        )
        self.user2.timezone = 'Pacific/Honolulu'
        self.user2.school = 'University of Hawaii at Manoa'
        self.user2.exempt_from_payment = True
        self.user2.save()

        # ############################################### Course Objects ###############################################

        self.course = Course.objects.create(
            name='CHEM 161',
            user=self.user,
            title='General Chemistry',
            teacher='Elijah Lopez',
            color='primary'
        )
        self.course2 = Course.objects.create(
            name='MATH 242',
            user=self.user2,
            title='Calculus 1',
            teacher='Jude Lopez',
            color='secondary'
        )
        self.coursetime = CourseTime.objects.create(
            course=self.course,
            user=self.user,
            location='KUY 310',
            start_time='12:00:00',
            end_time='13:15:00',
            weekday="['Tuesday', 'Thursday']"
        )

        # ############################################ Homework Assignments ############################################

        self.assignment = HomeworkAssignment.objects.create(
            name='Problems 1-10',
            course=self.course,
            due_date=datetime.date.today() + datetime.timedelta(days=3),
            due_time='23:59:00'
        )

        # ############################################## Calendar Events ###############################################

        self.event = CalendarEvent.objects.create(
            date=datetime.date.today() + datetime.timedelta(days=2),
            user=self.user,
            time='20:00:00',
            title='Test Event'
        )
        self.now = datetime.datetime.now(tz=pytz.timezone(self.user.timezone))
        self.today = self.now.date()
        self.today_time = datetime.time(self.now.hour, self.now.minute, 0)
