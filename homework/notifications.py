import datetime

import pytz
from django.template.loader import render_to_string

from base.decorators import register_class
from base.notifications import NotificationsConfig, Notification
from homework.models import HomeworkAssignment
from users.models import Account


@register_class()
class HomeworkDueInSixHoursNotifications(NotificationsConfig):
    user_constraints = {
        'homework_notifications': True,
        'timezone__isnull': False
    }
    _in_hours = 6

    def get_notifications(self, user):
        now = datetime.datetime.now(tz=pytz.timezone(user.timezone)) + datetime.timedelta(hours=self._in_hours)
        assignments = HomeworkAssignment.objects.filter(
            course__user=user,
            due_date=now.date(),
            due_time__hour=now.hour,
            due_time__minute=now.minute
        )
        if assignments.exists():
            subject = f'{assignments.count()} Homework Assignment{"s" if assignments.count() > 1 else ""} Due '
            if self._in_hours:
                subject += f'In {self._in_hours} Hours'
            else:
                subject += 'Now'
            self.current_notifications.append(Notification(
                subject=subject,
                message=render_to_string(
                    'email/homework_assignments.txt',
                    context={
                        'subject': subject,
                        'assignments': assignments
                    }
                ),
                recipient=user
            ))


@register_class()
class HomeworkDueNowNotifications(HomeworkDueInSixHoursNotifications):
    _in_hours = 0
