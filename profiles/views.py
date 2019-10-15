from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from login.models import Teacher, Student
from .forms import TeacherUpdateForm, StudentUpdateForm
from pymongo import MongoClient
# Create your views here.


@login_required
def profile_update(request):
    try:
        teacher = Teacher.objects.get(username=request.user)
    except:
        return render(request, 'registration/login.html')
    form = TeacherUpdateForm(request.POST or None, instance=teacher)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
        return render(request, 'profiles/teacher_profile.html', {'form': form})
    else:
        return render(request, 'profiles/teacher_profile.html', {'form': form})


@login_required
def student_profile_update(request, roll_no):
    student = Student.objects.get(roll_no=roll_no)
    if student:
        form = StudentUpdateForm(request.POST or None, instance=student)
        if form.is_valid():
            form.save()
        return render(request, 'profiles/student_profile.html', {'form': form})
    else:
        print("Invalid Roll No.")
        return render(request, 'profiles/student_profile.html', {'form': False})
    if request.method == 'POST':
        print('Here')


@login_required
def student_profile(request):
    client = MongoClient()
    db = client['attendance']
    collection = db['login_teacher']
    teacher = collection.find_one({'username':str(request.user)})
    if teacher != "N/A":
        collection = db['login_student']
        students = collection.find({'year': teacher['cc'], 'department': teacher['department']})
        students = list(students)
        if not students:
            students = False
    client.close()
    return render(request, 'profiles/student.html', {'students': students})


@login_required
def profile_view(request):
    client = MongoClient()
    db = client['attendance']
    col = db['login_teacher']
    teacher = col.find({'username': str(request.user)})
    client.close()
    return render(request, 'profiles/profile.html', {'teacher': teacher})


@login_required
def mentees(request):
    client = MongoClient()
    db = client['attendance']
    collection = db['login_teacher']
    teacher = collection.find_one({'username': str(request.user)}, {'name': 1})
    teacher = teacher['name']
    collection = db['login_student']
    students = collection.find({'teacher_guardian_id': teacher})
    client.close()
    students = list(students)
    if not students:
        students = False
    return render(request, 'profiles/mentees.html', {'students': students})
