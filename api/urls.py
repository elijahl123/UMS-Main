from django.urls import path

from api.views import CourseApiView

urlpatterns = [
    path('courses/view/', CourseApiView.as_view(), name='api_course_view')
]