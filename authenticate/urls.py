from django.urls import path
from . import views

urlpatterns = [
    path('',views.home, name='home'),
    path('logout',views.logout_user, name='logout'),
    path('auth_faculty', views.faculty_login_page, name='faculty_login_page'),
    path('auth_student', views.student_login_page, name='student_login_page'),
]