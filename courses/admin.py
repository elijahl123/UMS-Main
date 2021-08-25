from django.contrib import admin

# Register your models here.
from courses.models import *

admin.site.register(Course)
admin.site.register(CourseTime)
