from typing import List

from django.contrib.admin.sites import AlreadyRegistered
from django.core.mail import EmailMultiAlternatives, get_connection, send_mass_mail
from django.utils.module_loading import autodiscover_modules

from users.models import Account


class Notification:
    def __init__(
            self,
            subject: str,
            message: str,
            recipient: Account,
    ):
        self.subject = subject
        self.message = message
        self.recipient = recipient


class NotificationsFramework:
    def __init__(self):
        self._registry = []

    @staticmethod
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

    def collect(self):
        autodiscover_modules('notifications')

    def register(self, config):
        for i in self._registry:
            if isinstance(i, type(config)):
                raise AlreadyRegistered('This configuration is already registered')
        self._registry.append(config())

    def send_notifications(self):
        data_tuple = []
        data_tuple_html = []
        for config in self._registry:
            push_to = data_tuple_html if config.html else data_tuple
            push_to.extend(config.generate_tuple())
        send_mass_mail(data_tuple)
        self.send_mass_html_mail(data_tuple_html)


class NotificationsConfig:
    html: bool = False

    current_notifications: List[Notification] = []

    def get_notifications(self):
        pass

    def generate_tuple(self):
        self.get_notifications()
        return [
            (
                n.subject,
                n.message,
                n.message,
                'UMS Reminders <untitledmanagementsoftware@gmail.com>',
                [n.recipient.email]
            )
            for n in self.current_notifications
        ] if self.html else [
            (
                n.subject,
                n.message,
                'UMS Reminders <untitledmanagementsoftware@gmail.com>',
                [n.recipient.email]
            )
            for n in self.current_notifications
        ]


notifications_framework = NotificationsFramework()


def send_all_notifications():
    n = notifications_framework
    n.collect()
    n.send_notifications()
