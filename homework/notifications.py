import datetime

import pytz
from django.db.models import Count
from django.template.loader import render_to_string
from base.notifications import NotificationsConfig, Notification
from homework.models import HomeworkAssignment
from users.models import Account


class HomeworkNotifications(NotificationsConfig):

    def get_notifications(self):
        assignments_users = Account.objects.filter(
            homework_notifications=True,
            timezone__isnull=False
        )
        for user in assignments_users:
            assignments = HomeworkAssignment.objects.filter(
                course__user=user,
                completed=False
            )
            time = datetime.datetime.now(tz=pytz.timezone(user.timezone))
            now = datetime.datetime(
                time.year, time.month, time.day, time.hour, time.minute, 0
            )

            assignments_list = {}

            for assignment in assignments:
                if assignment.alert != -1:
                    alert = assignment.due_datetime - datetime.timedelta(minutes=assignment.alert)
                else:
                    alert = None
                if assignment.second_alert != -1:
                    second_alert = assignment.due_datetime - datetime.timedelta(minutes=assignment.second_alert)
                else:
                    second_alert = None
                if alert and alert == now:
                    val = assignments_list.get(assignment.alert, None)
                    if not val:
                        assignments_list[assignment.alert] = [assignment]
                    else:
                        assignments_list[assignment.alert].append(assignment)
                if second_alert and second_alert == now:
                    val = assignments_list.get(assignment.second_alert, None)
                    if not val:
                        assignments_list[assignment.second_alert] = [assignment]
                    else:
                        assignments_list[assignment.second_alert].append(assignment)

            for key, val in assignments_list.items():
                time_dict = {
                    0: "Now",
                    5: "in 5 minutes",
                    10: "in 10 minutes",
                    15: "in 15 minutes",
                    30: "in 30 minutes",
                    60: "in 1 hour",
                    120: "in 2 hours",
                    1440: "in 1 day",
                    2880: "in 2 days",
                    10080: "in 1 week"
                }
                subject = f'{len(val)} Homework Assignment{"s" if len(val) > 1 else ""} Due {time_dict.get(key, "Soon")}'
                self.current_notifications.add(Notification(
                    subject=subject,
                    message=render_to_string(
                        'email/homework_assignments.txt',
                        context={
                            'subject': subject,
                            'assignments': val
                        }
                    ),
                    recipient=user
                ))
