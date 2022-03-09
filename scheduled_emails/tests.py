# Create your tests here.
import datetime

from base.notifications import NotificationsFramework, NotificationsConfig
from base.tests import BaseTestCase
from homework.models import HomeworkAssignment


class ScheduledEmailTest(BaseTestCase):

    def setUp(self) -> None:
        super().setUp()

    def test_homework_notifications(self):
        in_six_hours = self.now + datetime.timedelta(hours=6)
        in_six_hours_assignment = HomeworkAssignment.objects.create(
            name='Notification Assignment Due in Six Hours',
            course=self.course,
            due_date=in_six_hours.date(),
            due_time=datetime.time(in_six_hours.hour, in_six_hours.minute, 0)
        )
        now_assignment = HomeworkAssignment.objects.create(
            name='Notification Assignment Due Right Now',
            course=self.course,
            due_date=self.today,
            due_time=self.today_time
        )
        in_six_hours_assignment_user2 = HomeworkAssignment.objects.create(
            name='Notification Assignment Due in Six Hours',
            course=self.course2,
            due_date=in_six_hours.date(),
            due_time=datetime.time(in_six_hours.hour, in_six_hours.minute, 0)
        )
        n = NotificationsFramework()
        n.send_notifications()
        for config in n.get_registry():
            config: NotificationsConfig
            if config.__class__.__name__ == "HomeworkDueInSixHoursNotifications":
                self.assertTrue(len(config.current_notifications) == 2)
            elif config.__class__.__name__ == "HomeworkDueNowNotifications":
                self.assertTrue(len(config.current_notifications) == 1)

