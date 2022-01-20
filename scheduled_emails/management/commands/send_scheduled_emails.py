from django.core.management import BaseCommand

from base.notifications import notifications_framework


class Command(BaseCommand):
    help = 'Send Scheduled Emails to Users'

    def handle(self, *args, **options):
        n = notifications_framework
        n.collect()
        n.send_notifications()
