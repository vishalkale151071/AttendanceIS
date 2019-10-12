from django import forms
from login.models import Teacher, Student


class TeacherUpdateForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ('name', 'email_id', 'primary_phone_no', 'secondary_phone_no', 'cc', 'department', 'subjects', 'labs')

class TeacherRegistrationForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ('name', 'email_id', 'primary_phone_no', 'secondary_phone_no', 'cc', 'department', 'subjects', 'labs')


class StudentUpdateForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ('roll_no', 'name', 'department', 'division', 'year', 'batch', 'teacher_guardian', 'email_id',
                  'primary_phone_no', 'parents_phone_no')


class StudentRegistrationForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ('roll_no', 'name', 'department', 'division', 'year', 'batch', 'teacher_guardian', 'email_id', 'primary_phone_no', 'parents_phone_no')
