from django.urls import path

from courses import views

urlpatterns = [
    path('view/<id>/', views.course_view, name='course_view'),
    path('assignments/view/<id>/', views.course_assignments, name='course_assignments'),
    path('files/view/<id>/', views.course_files, name='course_files'),
    path('files/add/<id>/', views.add_course_file, name='add_course_file'),
    path('files/edit/<id>/<file_id>/', views.add_course_file, name='edit_course_file'),
    path('files/delete/<id>/<file_id>/', views.delete_course_file, name='delete_course_file'),
    path('links/view/<id>/', views.course_links, name='course_links'),
    path('links/add/<id>/', views.add_course_link, name='add_course_link'),
    path('links/edit/<id>/<link_id>/', views.add_course_link, name='edit_course_link'),
    path('links/delete/<id>/<link_id>/', views.delete_course_link, name='delete_course_link'),
    path('coursetimes/view/<id>/', views.course_coursetimes, name='course_coursetimes'),
]