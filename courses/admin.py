from django.contrib import admin

# Register your models here.
from courses.models import *


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'user')
    list_filter = ('user',)


@admin.register(CourseTime)
class CourseTimeAdmin(admin.ModelAdmin):
    list_display = ('course', 'user')
    list_filter = ('user', 'course')


@admin.register(CourseFile)
class CourseFileAdmin(admin.ModelAdmin):
    list_display = ('course', 'title')
    list_filter = ('title', 'course')


@admin.register(CourseLink)
class CourseLinkAdmin(admin.ModelAdmin):
    list_display = ('course', 'title')
    list_filter = ('title', 'course')
