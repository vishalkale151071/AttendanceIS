from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from login.models import Teacher, Student
from .forms import TeacherUpdateForm, StudentUpdateForm
from pymongo import MongoClient
# Create your views here.


def profile_update(request):
    teacher = Teacher.objects.get(username=request.user)
    form = TeacherUpdateForm(request.POST or None, instance=teacher)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
        return render(request, 'profiles/teacher_profile.html', {'form': form})
    else:
        return render(request, 'profiles/teacher_profile.html', {'form': form})


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


def student_profile(request):
    students = Student.objects.all()
    return render(request, 'profiles/student.html', {'students': students})

@login_required
def profile_view(request):
    client = MongoClient()
    db = client['attendance']
    col = db['login_teacher']
    teacher = col.find({'username': str(request.user)})
    for x in teacher:
        teacher = x
    client.close()
    return render(request, 'profiles/profile.html', teacher)