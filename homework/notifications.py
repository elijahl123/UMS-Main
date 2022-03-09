import datetime

import pytz
from django.db.models import Count
from django.template.loader import render_to_string
from base.notifications import NotificationsConfig, Notification
from homework.models import HomeworkAssignment
from users.models import Account


class HomeworkDueInSixHoursNotifications(NotificationsConfig):
    _in_hours = 6

    def get_desired_time(self, account):
        return datetime.datetime.now(tz=pytz.timezone(account.timezone)) + datetime.timedelta(hours=self._in_hours)

    def get_notifications(self):
        assignments_users = HomeworkAssignment.objects.filter(
            completed=False,
            course__user__homework_notifications=True,
            course__user__timezone__isnull=False
        ).values('course__user').annotate(assignment_count=Count('course__user')).order_by()
        for user in assignments_users:
            account = Account.objects.get(id=user['course__user'])
            now = self.get_desired_time(account)
            assignments = HomeworkAssignment.objects.filter(
                course__user=account,
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
                self.current_notifications.add(Notification(
                    subject=subject,
                    message=render_to_string(
                        'email/homework_assignments.txt',
                        context={
                            'subject': subject,
                            'assignments': assignments
                        }
                    ),
                    recipient=account
                ))


class HomeworkDueNowNotifications(HomeworkDueInSixHoursNotifications):
    _in_hours = 0
