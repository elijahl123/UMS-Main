import json

from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from google.oauth2.credentials import Credentials

from UMSMain.get_settings import settings
from base.models import ApiMixin
from users.models import Account


# Create your models here.

class CalendarEvent(ApiMixin):
    date = models.DateField(null=True)
    user = models.ForeignKey(Account, null=True, on_delete=models.CASCADE)
    time = models.TimeField(help_text='Leave Blank if Event is All Day', null=True, blank=True)
    title = models.CharField(max_length=120, null=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title


class CalendarTokenManager(models.Manager):
    def get_credentials(self, user):
        if self.filter(user=user, token__isnull=False).exists():
            creds = Credentials.from_authorized_user_info(
                json.loads(CalendarToken.objects.get(user=user).token),
                settings.GOOGLE_API_CREDENTIALS)
            return creds
        return None

    def get_token(self, user):
        try:
            return json.loads(self.get(user=user, token__isnull=False).token)
        except ObjectDoesNotExist:
            return None


class CalendarToken(ApiMixin):
    objects = CalendarTokenManager()

    user = models.ForeignKey(Account, null=True, on_delete=models.CASCADE)
    token = models.JSONField(null=True)
