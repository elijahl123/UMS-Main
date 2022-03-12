# Create your tests here.
import datetime
import timeit

from base.notifications import NotificationsFramework, NotificationsConfig
from base.tests import BaseTestCase
from homework.models import HomeworkAssignment


class ScheduledEmailTest(BaseTestCase):

    def setUp(self) -> None:
        super().setUp()

    def test_homework_notifications(self):
        in_two_hours = self.now + datetime.timedelta(hours=2)
        in_two_hours_assignment = HomeworkAssignment.objects.create(
            name='Notification Assignment Due in Two Hours',
            course=self.course,
            due_date=in_two_hours.date(),
            due_time=datetime.time(in_two_hours.hour, in_two_hours.minute, 0),
            second_alert=120
        )
        in_two_hours_assignment2 = HomeworkAssignment.objects.create(
            name='Notification Assignment Due in Two Hours -- Two',
            course=self.course,
            due_date=in_two_hours.date(),
            due_time=datetime.time(in_two_hours.hour, in_two_hours.minute, 0),
            second_alert=120
        )
        now_assignment = HomeworkAssignment.objects.create(
            name='Notification Assignment Due Right Now',
            course=self.course,
            due_date=self.today,
            due_time=self.today_time,
        )
        in_two_hours_assignment_user2 = HomeworkAssignment.objects.create(
            name='Notification Assignment Due in Two Hours',
            course=self.course2,
            due_date=in_two_hours.date(),
            due_time=datetime.time(in_two_hours.hour, in_two_hours.minute, 0),
            second_alert=120
        )
        n = NotificationsFramework()
        n.send_notifications()

