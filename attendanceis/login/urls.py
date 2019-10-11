from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    path('signup/teacher/', views.teacher_signup, name='teacher_signup'),
    path('', auth_views.LoginView.as_view(), name='login'),
    path('signup/student/', views.student_signup, name='student_signup'),
    path('add-subject-lab/', views.add_subject_lab, name='add_subject_lab')
]
