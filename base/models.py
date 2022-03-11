from django.db import models

reminder_choices = [
        (-1, "None"),
        (0, "At time of event"),
        (5, "5 minutes Before"),
        (10, "10 minutes Before"),
        (15, "15 minutes Before"),
        (30, "30 minutes Before"),
        (60, "1 hour Before"),
        (120, "2 hours Before"),
        (1440, "1 day Before"),
        (2880, "2 days Before"),
        (10080, "1 week Before")
    ]


class ReminderMixin(models.Model):

    alert = models.IntegerField(choices=reminder_choices, default=0)
    second_alert = models.IntegerField(choices=reminder_choices, default=-1)

    def get_alert(self):
        return dict(reminder_choices).get(self.alert, f"{self.alert} minutes before")

    def get_second_alert(self):
        return dict(reminder_choices).get(self.second_alert, f"{self.second_alert} minutes before")

    class Meta:
        abstract = True
