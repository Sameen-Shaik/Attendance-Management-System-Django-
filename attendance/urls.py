from django.urls import path
from . import views
from uuid import UUID

urlpatterns = [
    path("student_dashboard/home", views.student_dashboard, name='student_dashboard'),
    path("faculty_dashboard/home", views.faculty_dashboard, name='faculty_dashboard'),
    path('take_attendance/', views.take_attendance, name='take_attendance'),
    path('take_attendance/<uuid:session_id>', views.take_attendance, name='take_attendance_with_session'),
    path('student_dashboard/view_attendance/', views.student_view_attendance, name='student_view_attendance'),
    path('faculty_view_attendance/', views.faculty_view_attendance, name='faculty_view_attendance'),
    path('faculty_view_attendance/<int:course_batch_id>/', views.faculty_view_attendance, name='faculty_view_attendance_course'),
    path('student_dashboard/reports/', views.student_reports, name='student_reports'),
    path('faculty_dashboard/reports/', views.faculty_reports, name='faculty_reports'),
    path('faculty_dashboard/reports/<int:course_batch_id>/', views.faculty_reports, name='faculty_reports_course'),
]
