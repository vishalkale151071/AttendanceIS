from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from login.models import Subject, Lab, Student
from pymongo import MongoClient
from django.utils.dateparse import parse_datetime
from .models import AttendanceSubject
# Create your views here.

# first form in attendance for selecting Subject or Lab
@login_required
def attendance_form(request):
    if request.method == 'POST':
        client = MongoClient()
        db = client['attendance']
        collection = db['login_teacher']
        if request.POST.get('choice') == 'subject':
            teacher = collection.find_one({'username': str(request.user)})
            subjects = teacher['subjects']
            client.close()
            return render(request, 'attendance/attendance_subject.html', {'subjects': subjects})
        elif request.POST.get('choice') == 'lab':
            teacher = collection.find_one({'username': str(request.user)})
            labs = teacher['labs']
            client.close()
            return render(request, 'attendance/attendance_lab.html', {'labs': labs})
    return render(request, 'attendance/attendance.html', {})


# function for making sublist from lists
def split_list(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]

# Form for Subject attendance
@login_required
def attendance_subject(request):
    if request.method == 'POST':
        name = request.POST.get('subject')
        date = request.POST.get('date')
        from_time = request.POST.get('from')
        to_time = request.POST.get('to')
        slots = request.POST.get('slots')

        client = MongoClient()
        db = client['attendance']
        collection = db['login_teacher']
        division = collection.find_one({'username': str(request.user)})
        division = division['subjects']
        for subject in division:
            if subject['subject_name_id'] == name:
                division = subject['division']
                break

        collection = db['login_subject']
        year = collection.find_one({'name': subject['subject_name_id']})
        year = year['year']

        collection = db['login_student']
        students = collection.aggregate([{'$match': {'division': division, 'year': year}},
                                         {'$project': {
                                            'roll_no': 1, 'division': 1, 'year': 1, 'no': {'$substr': ["$roll_no", 6, -1]}}
                                        }, {'$sort': {'no': 1}}
                                         ])
        s = []
        [s.append(x) for x in students]
        s = list(split_list(s, 2))
        context = {
            'subject': name,
            'division': division,
            'date': date,
            'from_time': from_time,
            'to_time': to_time,
            'slots': slots,
            'student_list': s
        }
        client.close()
        return render(request, 'attendance/attendance_form.html', context)
    else:
        return render(request, 'attendance/attendance.html', {})

# Form for Lab attendance
@login_required
def attendance_lab(request):
    if request.method == 'POST':
        name = request.POST.get('lab')
        date = request.POST.get('date')
        from_time = request.POST.get('from')
        to_time = request.POST.get('to')

        client = MongoClient()
        db = client['attendance']
        collection = db['login_teacher']
        batch = collection.find_one({'username': str(request.user)})
        batch = batch['labs']
        for lab in batch:
            if lab['lab_name_id'] == name:
                batch = lab['batch']
                break

        collection = db['login_lab']
        year = collection.find_one({'name': lab['lab_name_id']})
        year = year['year']

        collection = db['login_student']
        students = collection.aggregate([{'$match': {'batch': batch, 'year': year}},
                                         {'$project': {
                                             'roll_no': 1, 'batch': 1, 'year': 1,
                                             'no': {'$substr': ["$roll_no", 6, -1]}}
                                         }, {'$sort': {'no': 1}}
                                         ])
        s = []
        [s.append(x) for x in students]
        s = list(split_list(s, 2))
        context = {
            'lab': name,
            'batch': batch,
            'date': date,
            'from_time': from_time,
            'to_time': to_time,
            'student_list': s
        }
        client.close()
        return render(request, 'attendance/attendance_form_lab.html', context)
    else:
        return render(request, 'attendance/attendance.html', {})

# Fill attendance for subject
@login_required
def fill_attendance(request):
    data = request.POST.copy()
    subject = data.pop('subject')[0]
    division = data.pop('division')[0]
    date = data.pop('date')[0]
    date = parse_datetime(date + "T00:00:00.000Z")
    from_time = data.pop('from')[0]
    from_time = parse_datetime("1900-01-01T"+from_time+":00Z")
    to_time = data.pop('to')[0]
    to_time = parse_datetime("1900-01-01T" + to_time + ":00Z")
    slots = data.pop('slots')[0]
    try:
        data.pop('csrfmiddlewaretoken')
    except Exception:
        print('CSRF error detected')

    roll_no = []
    client = MongoClient()
    db = client['attendance']
    collection = db['login_subject']

    year = collection.find_one({'name': subject})
    year = year['year']

    collection = db['login_student']
    students = collection.aggregate([{'$match': {'division': division, 'year': year}},
                                     {'$project': {
                                         'roll_no': 1, 'no': {'$substr': ["$roll_no", 6, -1]}}
                                     }, {'$sort': {'no': 1}}
                                     ])
    for pair in data:
        roll_no.append(pair)
    attendance = []
    for student in students:
        if student['roll_no'] in roll_no:
            attendance.append(dict(roll_no=student['roll_no'], status='P'))
        else:
            attendance.append(dict(roll_no=student['roll_no'], status='AB'))
    collection = db['counter']
    sequence_value = collection.find_one({'_id': 'attendance_attendancesubject'})

    document = {
        'id': int(sequence_value['sequence_value']) + 1,
        'date': date,
        'from_time': from_time,
        'to_time': to_time,
        'subject': subject,
        'div': division,
        'slots': slots,
        'attendance': attendance
    }
    collection.update({'_id': 'attendance_attendancesubject'}, {'$inc': {'sequence_value': 1}})

    collection = db['attendance_attendancesubject']
    collection.insert_one(document)
    client.close()
    return render(request, 'attendance/fill.html', {})

# Fill attendance for lab
@login_required
def fill_attendance_lab(request):
    data = request.POST.copy()
    lab = data.pop('lab')[0]
    batch = data.pop('batch')[0]
    date = data.pop('date')[0]
    date = parse_datetime(date + "T00:00:00.000Z")
    from_time = data.pop('from')[0]
    from_time = parse_datetime("1900-01-01T"+from_time+":00Z")
    to_time = data.pop('to')[0]
    to_time = parse_datetime("1900-01-01T" + to_time + ":00Z")
    try:
        data.pop('csrfmiddlewaretoken')
    except Exception:
        print('CSRF error detected')

    roll_no = []
    client = MongoClient()
    db = client['attendance']
    collection = db['login_lab']

    year = collection.find_one({'name': lab})
    year = year['year']
    collection = db['login_student']
    students = collection.aggregate([{'$match': {'batch': batch, 'year': year}},
                                     {'$project': {
                                         'roll_no': 1, 'no': {'$substr': ["$roll_no", 6, -1]}}
                                     }, {'$sort': {'no': 1}}
                                     ])
    for pair in data:
        roll_no.append(pair)
    attendance = []
    for student in students:
        if student['roll_no'] in roll_no:
            attendance.append(dict(roll_no=student['roll_no'], status='P'))
        else:
            attendance.append(dict(roll_no=student['roll_no'], status='AB'))
    collection = db['counter']
    sequence_value = collection.find_one({'_id': 'attendance_attendancelab'})

    document = {
        'id': int(sequence_value['sequence_value']) + 1,
        'date': date,
        'from_time': from_time,
        'to_time': to_time,
        'lab': lab,
        'batch': batch,
        'attendance': attendance
    }
    collection.update({'_id': 'attendance_attendancelab'}, {'$inc': {'sequence_value': 1}})

    collection = db['attendance_attendancelab']
    collection.insert_one(document)
    client.close()
    return render(request, 'attendance/fill.html', {})