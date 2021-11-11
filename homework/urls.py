from django.urls import path

from homework.views import *

urlpatterns = [
    path('', homework, name='homework'),
    path('add-assignment/', AddAssignmentView.as_view(), name='add_assignment'),
    path('edit-assignment/<id>/', EditAssignmentView.as_view(), name='edit_assignment'),
    path('delete-assignment/<id>/', DeleteAssignmentView.as_view(), name='delete_assignment'),
    path('add-reading-assignment/', AddReadingAssignment.as_view(), name='add_reading_assignment'),
    path('edit-reading-assignment/<id>/', EditReadingAssignment.as_view(), name='edit_reading_assignment'),
    path('delete-reading-assignment/<id>/', DeleteReadingAssignment.as_view(), name='delete_reading_assignment'),
    path('complete-assignment/<id>/', CompleteAssignment.as_view(), name='complete_assignment'),
]
