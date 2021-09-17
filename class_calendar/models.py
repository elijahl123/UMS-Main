import json

from django.db import models
from google.oauth2.credentials import Credentials

from UMSMain.settings import GOOGLE_API_CREDENTIALS
from users.models import Account


# Create your models here.

class CalendarEvent(models.Model):
    date = models.DateField(null=True)
    user = models.ForeignKey(Account, null=True, on_delete=models.CASCADE)
    time = models.TimeField(help_text='Leave Blank if Event is All Day', null=True, blank=True)
    title = models.CharField(max_length=120, null=True)
    description = models.TextField(null=True, blank=True)


class CalendarTokenManager(models.Manager):
    def get_credentials(self, user):
        if self.filter(user=user, token__isnull=False).exists():
            creds = Credentials.from_authorized_user_info(
                json.loads(CalendarToken.objects.get(user=user).token),
                GOOGLE_API_CREDENTIALS)
            return creds
        return None


class CalendarToken(models.Model):
    objects = CalendarTokenManager()

    user = models.ForeignKey(Account, null=True, on_delete=models.CASCADE)
    token = models.JSONField(null=True)
