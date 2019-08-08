from django.shortcuts import render, HttpResponse
from pymongo import MongoClient
from .models import Teacher
def login(request):
    client = MongoClient()
    db = client['attendance']
    collection = db['login_teacher']
    data = collection.find_one()
    l = []
    for x in data:
        l.append(x)
    print(l)
    for i in l:
        print(data[i])
    return HttpResponse('<h1>Login Page</h1>')
