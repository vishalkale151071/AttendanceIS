from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponse
from django.utils.dateparse import parse_datetime
from pymongo import MongoClient
import csv


@login_required
def report(request):
    client = MongoClient()
    db = client['attendance']
    collection = db['login_teacher']

    teacher = collection.find_one({'username':str(request.user)})
    subjects = teacher['subjects']
    labs = teacher['labs']
    context = {
        'subjects': subjects,
        'labs': labs
    }
    return render(request, 'report/report.html', context)

@login_required
def subject_report(request):
    if request.method == 'POST':
        subject = request.POST.get('subject')
        division = request.POST.get(subject)
        from_date = request.POST.get('from_date')
        from_date = parse_datetime(from_date+"T00:00:00Z")
        to_date = request.POST.get('to_date')
        to_date= parse_datetime(to_date+"T00:00:00Z")
        client = MongoClient()
        db = client['attendance']
        collection = db['attendance_attendancesubject']

        data = collection.find({
            'subject': subject,
            '$and':[{'date': {'$gte':from_date, '$lte':to_date}}]
        },{'attendance': 1, 'date': 1})

        attendance = []
        [attendance.append(x) for x in data]
        head = ['roll_no']
        for x in attendance:
            head.append(str(x['date']))
            x.pop('date')
            x.pop('_id')

        sheet = {}
        for day in attendance:
            for x in day['attendance']:
                print(x)

        print(sheet)
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = "attachment; filename='report.csv'"

        writer = csv.writer(response)
        writer.writerow(head)
        for row in data['attendance']:
            writer.writerow([row['roll_no'], row['status']])

    return response


@login_required
def lab_report(request):
    return report(request)
