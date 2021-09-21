from django.contrib import admin

from class_calendar.models import *


# Register your models here.


@admin.register(CalendarEvent)
class CalendarEventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'user')
    list_filter = ('date', 'user')
