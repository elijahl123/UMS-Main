from dataclasses import dataclass, field, asdict
from typing import List, Set

from django.contrib.admin.sites import AlreadyRegistered
from django.core.mail import EmailMultiAlternatives, get_connection, send_mass_mail
from django.utils.module_loading import autodiscover_modules

from users.models import Account


@dataclass(frozen=True, order=True)
class Notification:
    subject: str
    message: str
    recipient: Account


class NotificationsConfig:
    html: bool = False

    current_notifications: Set[Notification] = set()

    def __repr__(self):
        out = ''
        for notification in self.current_notifications:
            pretty_print = 'Notification:\n' \
                          f'    subject: {notification.subject}\n' \
                          f'    message: {notification.message.encode()}\n' \
                          f'    recipient: {notification.recipient}\n'
            out += pretty_print
        return out

    def __hash__(self):
        return hash(tuple(self.current_notifications))

    def get_notifications(self):
        pass

    def generate_tuple(self):
        self.current_notifications = set()
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


class NotificationsFramework:

    def __init__(self):
        autodiscover_modules('notifications')
        self._registry = set()
        self.recursive_search_subclass(NotificationsConfig, self._registry)

    def print_registry(self):
        for val in self._registry:
            print(val)

    def get_registry(self):
        return self._registry

    def recursive_search_subclass(self, cls, iterable: set):
        for sub_cls in cls.__subclasses__():
            iterable.add(sub_cls())
            if sub_cls.__subclasses__():
                self.recursive_search_subclass(sub_cls, iterable)

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

    def send_notifications(self):
        data_tuple = []
        data_tuple_html = []
        for config in self._registry:
            if config.html:
                data_tuple_html.extend(config.generate_tuple())
            else:
                data_tuple.extend(config.generate_tuple())

        send_mass_mail(data_tuple)
        self.send_mass_html_mail(data_tuple_html)
