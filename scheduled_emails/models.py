from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

# Create your models here.
from users.models import Account


class AttachmentManager(models.Manager):
    use_for_related_fields = True

    def for_content_type(self, content_type: ContentType):
        return [obj.content_object for obj in self.filter(content_type=content_type)]


class Attachment(models.Model):
    objects = AttachmentManager()

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')


class ScheduledEmail(models.Model):
    date = models.DateField(null=True, blank=True)
    time = models.TimeField(null=True, blank=True)
    subject = models.CharField(max_length=120)
    template = models.TextField()
    context = models.JSONField(null=True, blank=True)
    recipient_list = models.ForeignKey(Account, on_delete=models.CASCADE)
    recurring = models.BooleanField(default=False)
    html = models.BooleanField(default=False)
    attachments = models.ManyToManyField(Attachment, blank=True)
