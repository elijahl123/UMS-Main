import datetime
import json

import pytz
from django.contrib.contenttypes.models import ContentType
from django.core.mail import EmailMultiAlternatives, get_connection, send_mass_mail
from django.core.management import BaseCommand
from django.template.loader import render_to_string

from base.notifications import Notifications, notifications_framework
from scheduled_emails.models import ScheduledEmail
from users.models import Account


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


class Command(BaseCommand):
    help = 'Send Scheduled Emails to Users'

    def handle(self, *args, **options):
        n = notifications_framework
        n.collect()
        data_tuple_html = []
        data_tuple = []


# data_tuple_html.append(
#     (
#         email.subject,
#         message,
#         message,
#         'UMS Reminders <untitledmanagementsoftware@gmail.com>',
#         [email.recipient_list.email]
#     )
# )
