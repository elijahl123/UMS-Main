from django.db import models

from base.models import ApiMixin
# Create your models here.
from courses.models import Course
from users.models import Account


class Note(ApiMixin):
    uploaded = models.DateField(auto_now_add=True)
    modified = models.DateField(auto_now=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=120, default='Untitled Document')
    content = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ['course', '-modified']

    def __str__(self):
        return self.title
