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
    cc = teacher['cc']
    dept = teacher['department']
    if cc == 'N/A':
        cc == False
    context = {
        'subjects': subjects,
        'labs': labs,
        'cc': cc,
        'dept': dept
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
    head.append('Total %')
    head.append('Defaulter')
    writer.writerow(head)
    total_lectures = len(head) -3
    for t in zip(*sheet):
        if "Total Present" not in t and "Total Absent" not in t:
            present = t.count('P')
            percent = (present / total_lectures * 100)
            percent = float("{0:.2f}".format(percent))
            t = list(t)
            t.append(percent)
            if percent < 75.00:
                t.append("Defaulter")
            else:
                t.append("Not Defaulter")
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
    head.append('Total %')
    head.append('Defaulter')
    writer.writerow(head)
    total_lectures = len(head) - 3
    for t in zip(*sheet):
        if "Total Present" not in t and "Total Absent" not in t:
            present = t.count('P')
            percent = (present / total_lectures * 100)
            percent = float("{0:.2f}".format(percent))
            t = list(t)
            t.append(percent)
            if percent < 75.00:
                t.append("Defaulter")
            else:
                t.append("Not Defaulter")
        writer.writerow(t)
    client.close()
    return response


@login_required
def class_report(request):
    if request.method == 'POST':
        department = request.POST.get('department')
        year = request.POST.get('year')
        sem = request.POST.get('sem')
        from_date = request.POST.get('from_date')
        from_date = parse_datetime(from_date + "T00:00:00Z")
        to_date = request.POST.get('to_date')
        to_date = parse_datetime(to_date + "T00:00:00Z")
        head = ['Roll No']

        client = MongoClient()
        db = client['attendance']

        collection = db['login_student']
        students = collection.aggregate(
            [{'$match': {'year': year, 'department': department}},
             {'$project': {
                 'roll_no': 1,
                 'no': {'$substr': ["$roll_no", 6, -1]}}
             }, {'$sort': {'no': 1}}
             ])
        students_list = []
        [students_list.append(x['roll_no']) for x in students]

        collection = db['login_subject']
        subjects = collection.find({'year':year, 'dept': department, 'sem': sem}, {'name': 1})
        subject_list = []
        for x in subjects:
            subject_list.append(x['name'])


        collection = db['login_lab']
        labs = collection.find({'year': year, 'dept': department, 'sem': sem}, {'name': 1})
        lab_list = []
        for x in labs:
            lab_list.append(x['name'])
        attendance_subject = []
        attendance_lab = []
        collection = db['attendance_attendancesubject']
        subject_attendance = collection.find({'year':year, '$and': [{'date': {'$gte': from_date, '$lte': to_date}}]}, {'attendance': 1, 'subject': 1}).sort([('subject', 1)])
        [attendance_subject.append(x) for x in subject_attendance]

        collection = db['attendance_attendancelab']
        lab_attendance = collection.find({'year':year, '$and': [{'date': {'$gte': from_date, '$lte': to_date}}]}, {'attendance': 1, 'lab': 1}).sort([('lab', 1)])
        [attendance_lab.append(x) for x in lab_attendance]
        datasheet = []
        total_lectures = []
        for subject in subject_list:
            head.append(subject)
            sheet = list(filter(lambda k:k['subject'] == subject, attendance_subject))
            att = []
            for s in sheet:
                attendance_subject.remove(s)
                s = s['attendance']
                att.append(s)
            data = []
            total_lectures.append(len(att))
            for student in students_list:
                d = dict(roll_no=student, status='P')
                p = 0
                for attendance in att:
                    if d in attendance:
                        p += 1
                data.append(p)
            datasheet.append(data)

        for lab in lab_list:
            head.append(lab)
            sheet = list(filter(lambda k:k['lab'] == lab, attendance_lab))
            att = []
            for s in sheet:
                attendance_lab.remove(s)
                s = s['attendance']
                att.append(s)
            data = []
            total_lectures.append(len(att))
            for student in students_list:
                d = dict(roll_no=student, status='P')
                p = 0
                for attendance in att:
                    if d in attendance:
                        p += 1
                data.append(p)
            datasheet.append(data)

        datasheet.insert(0, students_list)

        head.append("Total %")
        head.append("Defaulter")

        # Write csv
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = "attachment; filename=report.csv"
        writer = csv.writer(response)
        writer.writerow(head)
        print(total_lectures)
        for t in zip(*datasheet):
            writer.writerow(t)
        client.close()
        return response