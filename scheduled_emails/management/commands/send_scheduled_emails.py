import datetime

import pytz
from django.core.mail import EmailMultiAlternatives, get_connection
from django.core.management import BaseCommand
from django.template.loader import render_to_string
from pytz import timezone

from courses.models import CourseTime
from homework.models import HomeworkAssignment
from scheduled_emails.models import ScheduledEmail


def send_mass_html_mail(datatuple, fail_silently=False, user=None, password=None,
                        connection=None):
    """
    Given a datatuple of (subject, text_content, html_content, from_email,
    recipient_list), sends each message to each recipient list. Returns the
    number of emails sent.

    If from_email is None, the DEFAULT_FROM_EMAIL setting is used.
    If auth_user and auth_password are set, they're used to log in.
    If auth_user is None, the EMAIL_HOST_USER setting is used.
    If auth_password is None, the EMAIL_HOST_PASSWORD setting is used.

    """
    connection = connection or get_connection(
        username=user, password=password, fail_silently=fail_silently)
    messages = []
    for subject, text, html, from_email, recipient in datatuple:
        message = EmailMultiAlternatives(subject, text, from_email, recipient)
        message.attach_alternative(html, 'text/html')
        messages.append(message)
    return connection.send_messages(messages)


def get_daily_summary_tuple(user):
    tomorrow_weekday = (datetime.datetime.now(timezone(user.timezone)) + datetime.timedelta(days=1)).strftime("%A")
    coursetimes = CourseTime.objects.filter(
        course__user=user,
        weekday__contains=tomorrow_weekday
    )
    upcoming_assignments = HomeworkAssignment.objects.upcoming_assignments(user)

    html_message = render_to_string('email/daily_summary.html', context={'account': user, 'coursetimes': coursetimes,
                                                                         'upcoming_assignments': upcoming_assignments})
    return (
        'Daily Summary',
        html_message,
        html_message,
        'UMS Reminders <untitledmanagementsoftware@gmail.com>',
        [user.email]
    )


class Command(BaseCommand):
    help = 'Send Scheduled Emails to Users'

    def handle(self, *args, **options):
        data_tuple = []
        for email in ScheduledEmail.objects.all():

            now = datetime.datetime.now()
            if email.recipient_list.timezone:
                now = datetime.datetime.now(pytz.timezone(email.recipient_list.timezone))

            today = datetime.date(now.year, now.month, now.day)
            time = datetime.time(now.hour, now.minute, 0)

            if (email.date and email.date == today) or email.recurring:
                if email.time == time:
                    data_tuple.append(
                        (
                            email.subject,
                            email.message,
                            email.message,
                            'UMS Reminders <untitledmanagementsoftware@gmail.com>',
                            [email.recipient_list.email]
                        )
                    )

            if not email.recurring:
                email.delete()

        send_mass_html_mail(tuple(data_tuple))
