from django.contrib.auth import authenticate
from django.shortcuts import render, HttpResponse
from pymongo import MongoClient
from django.views import generic
from django.urls import reverse_lazy
from .forms import TeacherRegistrationForm, UserForm


def login(request):
    return render(request, 'login/login.html', {})


def verify(request):
    if request.method == 'POST':
        username = request.POST.get('uname')
        password = request.POST.get('psw')

        auth = authenticate(usename=username, password=password)
        print(auth)

def signup(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_data = TeacherRegistrationForm(data=request.POST)
        if profile_data.is_valid() and user_form.is_valid():
            user_rs = user_form.save()
            user_rs.set_password(user_rs.password)
            user_rs.save()
            profile_rs = profile_data.save(commit=False)
            profile_rs.user = user_rs
            profile_rs.username = user_rs
            profile_rs.save()
            registered = True
            return render(request, 'url : login', {})
        else:
            print("INVALID")

    return render(request, 'login/signup.html', { 'form': UserForm, 'extra_form': TeacherRegistrationForm, 'rs':registered})