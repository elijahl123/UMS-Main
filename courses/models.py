from django.db import models

from school.models import School
from users.models import Account

# Create your models here.
color_choices = [
    ('primary', 'Blue'),
    ('secondary', 'Gray'),
    ('success', 'Green'),
    ('danger', 'Red'),
    ('warning', 'Yellow'),
    ('info', 'Light Blue'),
]

def upload_course_file(instance, filename):
    file_path = 'course_files/{username}/{filename}'.format(
        username=str(instance.course.user.username), filename=filename
    )
    return file_path


class Course(models.Model):
    name = models.CharField(blank=False, null=True, max_length=120,
                            help_text='Name of Class (CHEM 161, POLS 110, etc.)')
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(blank=True, null=True, max_length=120,
                             help_text='Full Name of Class (General Chemistry I, etc.)')
    teacher = models.CharField(blank=False, null=True, max_length=120)
    school = models.ForeignKey(School, on_delete=models.CASCADE, null=True, blank=True)
    color = models.TextField(max_length=120, default='primary', choices=color_choices,
                             help_text='Color You Want This Class to Show Up as on Calendar and Schedule')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        unique_together = ['user', 'name']


class CourseTime(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True, blank=True)
    location = models.TextField(blank=True, null=True, help_text='Leave Blank if Class is Online')
    start_time = models.TimeField(blank=False, null=True)
    end_time = models.TimeField(blank=False, null=True)
    weekday = models.TextField(max_length=120, default='Sunday', verbose_name='Weekdays')
    link = models.URLField(max_length=500, null=True, blank=True)
    zoom_password = models.TextField(max_length=120, null=True, blank=True)

    def __str__(self):
        return self.course.name

    def weekdays(self):
        return self.weekday[1:-1].replace('\'', '')

    class Meta:
        ordering = ['start_time']


class CourseFile(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(null=True, max_length=120)
    file = models.FileField(null=True, upload_to=upload_course_file)
    uploaded = models.DateTimeField(auto_now_add=True)
