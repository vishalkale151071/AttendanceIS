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

    teacher = collection.find_one({'username': str(request.user)})
    subjects = teacher['subjects']
    labs = teacher['labs']
    context = {
        'subjects': subjects,
        'labs': labs
    }
    client.close()
    return render(request, 'report/report.html', context)


@login_required
def subject_report(request):
    if request.method == 'POST':
        subject = request.POST.get('subject')
        division = request.POST.get(subject)
        from_date = request.POST.get('from_date')
        from_date = parse_datetime(from_date + "T00:00:00Z")
        to_date = request.POST.get('to_date')
        to_date = parse_datetime(to_date + "T00:00:00Z")
        client = MongoClient()
        db = client['attendance']
        collection = db['attendance_attendancesubject']

        data = collection.find({
            'subject': subject,
            '$and': [{'date': {'$gte': from_date, '$lte': to_date}}]
        }, {'attendance': 1, 'date': 1, 'slots': 1}).sort([('date', 1)])

        attendance = []
        [attendance.append(x) for x in data]
        head = ['roll_no']

        collection = db['login_subject']
        sub = collection.find_one({'name': subject}, {'dept': 1, 'year': 1})

        collection = db['login_student']
        students = collection.aggregate(
            [{'$match': {'division': division, 'year': sub['year'], 'department': sub['dept']}},
             {'$project': {
                 'roll_no': 1,
                 'no': {'$substr': ["$roll_no", 6, -1]}}
             }, {'$sort': {'no': 1}}
             ])
        students_list = []
        [students_list.append(x['roll_no']) for x in students]
        sheet = [students_list]
        for day in attendance:
            slots = int(day['slots'])
            for i in range(slots):
                head.append(day['date'].strftime("%m/%d/%Y"))
                row = []
                for roll_no in students_list:
                    no = next(item for item in day['attendance'] if item["roll_no"] == roll_no)
                    row.append(no['status'])
                    if not no:
                        row.append('AB')
                sheet.append(row)
        for row in sheet:
            p = row.count('P')
            a = row.count('AB')
            if p == 0:
                row.append("Total Present")
            else:
                row.append(p)
            if a == 0:
                row.append("Total Absent")
            else:
                row.append(a)
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = "attachment; filename=report.csv"
        writer = csv.writer(response)
        writer.writerow(head)
        for t in zip(*sheet):
            writer.writerow(t)
    return response


@login_required
def lab_report(request):
    if request.method == 'POST':
        lab = request.POST.get('lab')
        batch = request.POST.get(lab)
        from_date = request.POST.get('from_date')
        from_date = parse_datetime(from_date + "T00:00:00Z")
        to_date = request.POST.get('to_date')
        to_date = parse_datetime(to_date + "T00:00:00Z")
        client = MongoClient()
        db = client['attendance']
        collection = db['attendance_attendancelab']

        data = collection.find({
            'lab': lab,
            '$and': [{'date': {'$gte': from_date, '$lte': to_date}}]
        }, {'attendance': 1, 'date': 1, 'slots': 1}).sort([('date', 1)])

        attendance = []
        [attendance.append(x) for x in data]
        head = ['roll_no']

        collection = db['login_lab']
        Lab = collection.find_one({'name': lab}, {'dept': 1, 'year': 1})

        collection = db['login_student']
        students = collection.aggregate(
            [{'$match': {'batch': batch, 'year': Lab['year'], 'department': Lab['dept']}},
             {'$project': {
                 'roll_no': 1,
                 'no': {'$substr': ["$roll_no", 6, -1]}}
             }, {'$sort': {'no': 1}}
             ])
        students_list = []
        [students_list.append(x['roll_no']) for x in students]
        sheet = [students_list]
        for day in attendance:
            head.append(day['date'].strftime("%m/%d/%Y"))
            row = []
            for roll_no in students_list:
                no = next(item for item in day['attendance'] if item["roll_no"] == roll_no)
                row.append(no['status'])
                if not no:
                    row.append('AB')
            sheet.append(row)
        for e, row in enumerate(sheet):
            p = row.count('P')
            a = row.count('AB')
            if p == 0 and e == 0:
                row.append("Total Present")
            else:
                row.append(p)
            if a == 0 and e == 0:
                row.append("Total Absent")
            else:
                row.append(a)
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = "attachment; filename=report.csv"
        writer = csv.writer(response)
        writer.writerow(head)
        for t in zip(*sheet):
            writer.writerow(t)
        client.close()
    return response
