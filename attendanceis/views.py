from django.contrib.auth.decorators import login_required
from django.utils.dateparse import parse_datetime
from pymongo import MongoClient
from django.shortcuts import render
import matplotlib.pyplot as plt
import numpy as np


@login_required
def home(request):
    client = MongoClient()
    db = client['attendance']
    collection = db['login_teacher']
    teacher = collection.find_one({'username': str(request.user)})
    subjects = teacher['subjects']
    labs = teacher['labs']
    collection = db['login_subject']
    data = []
    reports = []
    for subject in subjects:
        sub = collection.find_one({'name': subject['subject_name_id']},{'name': 1, 'year': 1})
        sub['division'] = subject['division']
        data.append(sub)
    subjects = data
    collection = db['attendance_attendancesubject']
    for subject in subjects:
        attendance = collection.find({'subject': subject['name'], 'division': subject['division']},{'attendance': 1, 'date':1}).sort([('date', -1)]).limit(5)
        count = 0
        sum_of_p, sum_of_a, dates = [], [], []
        for one in attendance:
            count += 1
            att = one['attendance']
            p, a = 0, 0
            for x in att:
                if x['status'] == 'AB':
                    a += 1
                else:
                    p += 1
            sum_of_a.append(a)
            sum_of_p.append(p)
            dates.append(one['date'].strftime("%m/%d/%Y"))
        d = dict(name=subject['name'], dates=dates, present=sum_of_p, absent=sum_of_a, total=count)
        reports.append(d)
    graphs = []

    # lab reports
    data = []
    collection = db['login_lab']
    for lab in labs:
        Lab = collection.find_one({'name': lab['lab_name_id']},{'name': 1, 'year': 1})
        Lab['batch'] = lab['batch']
        data.append(Lab)
    labs = data
    collection = db['attendance_attendancelab']
    for lab in labs:
        attendance = collection.find({'lab': lab['name'], 'batch': lab['batch']},{'attendance': 1, 'date':1}).sort([('date', -1)]).limit(5)
        count = 0
        sum_of_p, sum_of_a, dates = [], [], []
        for one in attendance:
            count += 1
            att = one['attendance']
            p, a = 0, 0
            for x in att:
                if x['status'] == 'AB':
                    a += 1
                else:
                    p += 1
            sum_of_a.append(a)
            sum_of_p.append(p)
            dates.append(one['date'].strftime("%m/%d/%Y"))
        d = dict(name=lab['name'], dates=dates, present=sum_of_p, absent=sum_of_a, total=count)
        reports.append(d)
    # graph plotting logi
    for report in reports:
        print(report)
        labels = report['dates']
        present = report['present']
        absent = report['absent']

        x = np.arange(len(labels))  # the label locations
        width = 0.35  # the width of the bars

        fig, ax = plt.subplots()
        rects1 = ax.bar(x - width / 2, present, width, label='Presnt')
        rects2 = ax.bar(x + width / 2, absent, width, label='Absent')

        # Add some text for labels, title and custom x-axis tick labels, etc.
        ax.set_ylabel('Students')
        ax.set_xlabel(report['name'])
        ax.set_title('Attendance of last five lectures')
        ax.set_xticks(x)
        ax.set_xticklabels(labels)
        ax.set_ylim([0,45])
        ax.legend()

        def autolabel(rects):
            """Attach a text label above each bar in *rects*, displaying its height."""
            for rect in rects:
                height = rect.get_height()
                ax.annotate('{}'.format(height),
                            xy=(rect.get_x() + rect.get_width() / 2, height),
                            xytext=(0, 3),  # 3 points vertical offset
                            textcoords="offset points",
                            ha='center', va='bottom')

        autolabel(rects1)
        autolabel(rects2)
        fig.tight_layout()
        path = 'static/images/plot/'+ str(request.user) +report['name'] +'.png'
        plt.savefig(path)
        avg = sum(report['present'])//report['total']
        d = dict(image=path, name=report['name'], avg=avg)
        graphs.append(d)
        plt.close()
    client.close()
    return render(request, 'home.html', {'reports': graphs})