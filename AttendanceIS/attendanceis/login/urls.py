from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('verify/', views.verify, name='verify'),
    path('signup/', views.SignUp.as_view(), name='signup')
]
