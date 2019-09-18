from django import forms
from django.contrib.auth.models import User
from .models import Teacher,Student

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'password')


class TeacherRegistrationForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ('name', 'email_id', 'primary_phone_no', 'secondary_phone_no', 'tg', 'cc', 'subjects', 'labs')


class StudentRegistrationForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ('roll_no', 'name', 'department', 'division', 'year', 'batch', 'teacher_guardian', 'email_id', 'primary_phone_no', 'parents_phone_no')