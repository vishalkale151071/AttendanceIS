from django import forms
from django.contrib.auth.models import User
from .models import Teacher, Student, Subject, Lab

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), help_text= "1.Lenght 8 char. 2.use Char, Digits, Special symbols (@,#,$,%,&,*,_,-,+)")
    password_confirm = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'password', 'password_confirm')


class TeacherRegistrationForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ('name', 'email_id', 'primary_phone_no', 'secondary_phone_no', 'tg', 'cc', 'subjects', 'labs')


class StudentRegistrationForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ('roll_no', 'name', 'department', 'division', 'year', 'batch', 'teacher_guardian', 'email_id', 'primary_phone_no', 'parents_phone_no')


class SubjectFrom(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ('code', 'name', 'dept', 'year')


class LabFrom(forms.ModelForm):
    class Meta:
        model = Lab
        fields = ('code', 'name', 'dept', 'year')