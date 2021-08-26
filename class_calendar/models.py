from django.db import models

# Create your models here.
from django.utils import timezone

from users.models import Account


class CalendarEvent(models.Model):
    date = models.DateField(null=True)
    user = models.ForeignKey(Account, null=True, on_delete=models.CASCADE)
    time = models.TimeField(help_text='Leave Blank if Event is All Day', null=True, blank=True)
    title = models.CharField(max_length=120, null=True)
    description = models.TextField(null=True, blank=True)
