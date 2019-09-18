from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('verify/', views.verify, name='verify'),
    path('signup/', views.signup, name='signup')
]
