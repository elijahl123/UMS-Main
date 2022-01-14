from django.db import models

# Create your models here.
from users.models import Account


class ScheduledEmail(models.Model):
    date = models.DateField(null=True, blank=True)
    time = models.TimeField(null=True, blank=True)
    subject = models.CharField(max_length=120)
    message = models.TextField()
    recipient_list = models.ForeignKey(Account, on_delete=models.CASCADE)
    recurring = models.BooleanField(default=False)
    html = models.BooleanField(default=False)