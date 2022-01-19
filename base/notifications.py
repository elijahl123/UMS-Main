import datetime

from django.contrib.admin.sites import AlreadyRegistered
from django.utils.module_loading import autodiscover_modules

from users.models import Account


class Notifications:
    def __init__(self):
        self._registry = []

    def collect(self):
        autodiscover_modules('notifications')
        print(self._registry)

    def register(self, config):
        if config in self._registry:
            raise AlreadyRegistered('This configuration is already registered')

        self._registry.append(config)


class NotificationsConfig:
    html: bool = False
    template: str = None

    current_notifications = []

    def generate_tuple(self):
        pass


class Notification:
    def __init__(
            self,
            date: datetime.date = None,
            time: datetime.time = None,
            subject: str = None,
            recipient: Account = None
    ):
        self.date = date
        self.time = time
        self.subject = subject
        self.recipient = recipient


notifications_framework = Notifications()
