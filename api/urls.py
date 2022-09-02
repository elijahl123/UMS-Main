from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from api.views import *

urlpatterns = [
    path('courses/view/', CourseApiView.as_view(), name='api_course_view'),
    path('assignments/view/', AssignmentApiView.as_view(), name='api_assignment_view'),
    path('coursetimes/view/', CoursetimeApiView.as_view(), name='api_coursetime_view'),

    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]