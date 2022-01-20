# Create your tests here.
import datetime

from base.notifications import send_all_notifications
from base.tests import BaseTestCase
from homework.models import HomeworkAssignment


class ScheduledEmailTest(BaseTestCase):

    def setUp(self) -> None:
        super().setUp()

    def test_homework_notifications(self):
        in_six_hours = self.now + datetime.timedelta(hours=6)
        new_assignment = HomeworkAssignment.objects.create(
            name='Notification Assignment',
            course=self.course,
            due_date=in_six_hours.date(),
            due_time=datetime.time(in_six_hours.hour, in_six_hours.minute, 0)
        )
        send_all_notifications()
