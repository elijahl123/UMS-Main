from django.db import models

# Create your models here.
from django.utils.text import slugify


def upload_logo(instance, filename):
    file_path = 'logo/{name}/{filename}'.format(
        name=str(slugify(instance.name)), filename=filename
    )
    return file_path


class School(models.Model):
    name = models.CharField(blank=False, null=True, max_length=120, unique=True)
    logo = models.ImageField(upload_to=upload_logo, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
