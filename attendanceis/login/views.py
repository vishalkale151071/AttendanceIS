from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .forms import TeacherRegistrationForm, UserForm, StudentRegistrationForm, SubjectFrom, LabFrom


def teacher_signup(request):
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_data = TeacherRegistrationForm(data=request.POST)
        if profile_data.is_valid() and user_form.is_valid():
            if user_form.cleaned_data['password'] == user_form.cleaned_data['password_confirm']:
                user_rs = user_form.save()
                user_rs.set_password(user_rs.password)
                user_rs.save()
                profile_rs = profile_data.save(commit=False)
                profile_rs.user = user_rs
                profile_rs.username = user_rs
                profile_rs.save()
            else:
                print("password does not matches.")
                return render(request, 'login/signup.html', {'form': UserForm, 'extra_form': TeacherRegistrationForm, 'cperror':"password does not matches."})
            return render(request, 'home.html', {})
        else:
            print("INVALID form data")
            return render(request, 'login/signup.html', {'form': UserForm, 'extra_form': TeacherRegistrationForm})
    else:
        return render(request, 'login/signup.html', {'form': UserForm, 'extra_form': TeacherRegistrationForm})


def student_signup(request):
    if request.method == 'POST':
        student_form = StudentRegistrationForm(data=request.POST)
        if student_form.is_valid():
            student_info = student_form.save()
        return render(request, 'home.html', {})
    else:
        return render(request, 'login/student_signup.html', {'form': StudentRegistrationForm})


@login_required
def add_subject_lab(request):
    if request.method == 'POST':
        if request.POST.get('form') == 'subject':
            form = SubjectFrom(data=request.POST)
            save = form.save()
            return render(request, 'login/add_subject.html', {'subject': True, 'form': SubjectFrom})
        if request.POST.get('form') == 'lab':
            print('lab form fiiled.')
            form = LabFrom(data=request.POST)
            save = form.save()
            return render(request, 'login/add_subject.html', {'lab': True, 'form': LabFrom})
        if request.POST.get('ch') == 'subject':
            return render(request, 'login/add_subject.html', {'subject':True,'form':SubjectFrom})
        if request.POST.get('ch') == 'lab':
            return render(request, 'login/add_subject.html', {'lab':True,'form':LabFrom})
    else:
        return render(request, 'login/add_subject.html', {})