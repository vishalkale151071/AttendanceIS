from django.shortcuts import render, HttpResponse
from pymongo import MongoClient


def login(request):

    return render(request, 'login/login.html', {})


def verify(request):
    client = MongoClient()
    db = client['attendance']
    collection = db['login_teacher']
    query = {'name':'{}'.format(request.POST.get('uname'))}
    data = collection.find(query)

    if data.count():
        return HttpResponse('<h1>Valid</h1>')
    else:
        return HttpResponse('<h1>Invalid</h1>')