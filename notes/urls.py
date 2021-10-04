from django.urls import path

from notes import views

urlpatterns = [
    path('', views.notes_home, name='notes_home'),
    path('course/<course_id>/', views.notes_home_course, name='notes_home_course'),
    path('course/<course_id>/add/', views.add_notes, name='notes_add_notes'),
    path('course/<course_id>/view/<notes_id>/', views.view_notes, name='notes_view_notes'),
    path('course/<course_id>/delete/<notes_id>/', views.delete_notes, name='notes_delete_notes'),
]
