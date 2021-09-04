from django.urls import path

from api.views import *

urlpatterns = [
    path('courses/view/', CourseApiView.as_view(), name='api_course_view'),
    path('assignments/view/', AssignmentApiView.as_view(), name='api_assignment_view')
]