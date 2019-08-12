from django.contrib.auth import authenticate
from django.shortcuts import render, HttpResponse
from pymongo import MongoClient
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
import crypt

def login(request):

    return render(request, 'login/login.html', {})


def verify(request):
    if request.method == 'POST':
        username = request.POST.get('uname')
        password = request.POST.get('psw')

        auth = authenticate(usename=username, password=password)
        print(auth)

class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'login/signup.html'
