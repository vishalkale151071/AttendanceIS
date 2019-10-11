from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    path('', views.attendance_form, name='attendance'),
    path('subject/', views.attendance_subject, name='attendance_subject'),
    path('subject/fill', views.fill_attendance, name='attendance_subject_fill'),
    path('lab/fill', views.fill_attendance_lab, name='attendance_lab_fill'),
    path('lab/', views.attendance_lab, name='attendance_lab'),
]
