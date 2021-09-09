from django.db import models

from users.models import Account


# Create your models here.


class CalendarEvent(models.Model):
    date = models.DateField(null=True)
    user = models.ForeignKey(Account, null=True, on_delete=models.CASCADE)
    time = models.TimeField(help_text='Leave Blank if Event is All Day', null=True, blank=True)
    title = models.CharField(max_length=120, null=True)
    description = models.TextField(null=True, blank=True)


class CalendarToken(models.Model):
    user = models.ForeignKey(Account, null=True, on_delete=models.CASCADE)
    token = models.JSONField(null=True)
