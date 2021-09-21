from django.contrib import admin

# Register your models here.
from homework.models import *


@admin.register(HomeworkAssignment)
class HomeworkAssignmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'course', 'due_date', 'course_user')
    list_filter = ('course',)

    def course_user(self, obj):
        return obj.course.user

    course_user.short_description = 'User'


@admin.register(ReadingAssignment)
class ReadingAssignmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'course', 'due_date', 'course_user')
    list_filter = ('course',)

    def course_user(self, obj):
        return obj.course.user

    course_user.short_description = 'User'
