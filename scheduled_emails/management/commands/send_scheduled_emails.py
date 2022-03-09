from django.core.management import BaseCommand

from base.notifications import NotificationsFramework


class Command(BaseCommand):
    help = 'Send Scheduled Emails to Users'

    def handle(self, *args, **options):
        n = NotificationsFramework()
        n.send_notifications()
        n.print_registry()