from django.contrib.auth.models import User
from djongo import models


class Subjects(models.Model):
    subject_code = models.CharField(max_length=7)
    subject_name = models.CharField(max_length=100)

    class Meta:
        abstract = True


class Lab(models.Model):
    lab_code = models.CharField(max_length=7)
    lab_name = models.CharField(max_length=100)

    class Meta:
        abstract = True


class Teacher(models.Model):
    name = models.CharField(max_length=80)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=50)
    email_id = models.CharField(max_length=50)
    primary_phone_no = models.CharField(max_length=10)
    secondary_phone_no = models.CharField(max_length=10)
    tg = models.BooleanField(default=False)
    cc = models.BooleanField(default=False)
    subjects = models.ArrayModelField(model_container=Subjects)
    labs = models.ArrayModelField(model_container=Lab)


class Student(models.Model):
    roll_no = models.CharField(max_length=12, blank=False, primary_key=True, null=False)
    name = models.CharField(max_length=100)
    department = models.CharField(max_length=10)
    division = models.CharField(max_length=2)
    year = models.CharField(max_length=3)
    batch = models.CharField(max_length=2)
    teacher_guardian = models.CharField(max_length=100)
    email_id = models.EmailField(max_length=100)
    primary_phone_no = models.CharField(max_length=10)
    parents_phone_no = models.CharField(max_length=10)