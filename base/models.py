import uuid

from django.db import models


class UUIDModelHelper:
    app: str
    model: str

    def __init__(self, app: str, model: str):
        self.app = app
        self.model = model

    def gen_uuid(self, apps, schema_editor):
        model_obj = apps.get_model(self.app, self.model)
        for row in model_obj.objects.all():
            row.uuid = uuid.uuid4()
            row.save(update_fields=['uid'])


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


class ApiMixin(models.Model):
    uid = models.UUIDField(null=True, default=uuid.uuid4)

    def get_uid(self) -> uuid.UUID:
        if self.uid is None:
            self.uid = uuid.uuid4()
            self.save(update_fields=['uid'])
        return self.uid

    class Meta:
        abstract = True
