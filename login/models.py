from django.contrib.auth.models import User
from djongo import models


class Subject(models.Model):
    dept_choices = (
        ('comp', 'Computer Engineering'),
        ('civil', 'Civil Engineering'),
        ('mech', 'Mechanical Engineering'),
        ('it', 'Information Technology Engineering'),
        ('e&tc', 'E&TC Engineering'),
        ('inst', 'Instrumental Engineering'),
        ('prod', 'Production Engineering'),
    )
    sem_choices = (('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'))
    year_choices = (('F.E', 'F.E'), ('S.E', 'S.E'), ('T.E', 'T.E'), ('B.E', 'B.E'))

    code = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    dept = models.CharField(max_length=50, choices=dept_choices)
    year = models.CharField(max_length=3, choices=year_choices)
    sem = models.CharField(max_length=1, choices=sem_choices)

    def __str__(self):
        return self.code + " " + self.name


class Lab(models.Model):
    dept_choices = (
        ('comp', 'Computer Engineering'),
        ('civil', 'Civil Engineering'),
        ('mech', 'Mechanical Engineering'),
        ('it', 'Information Technology Engineering'),
        ('e&tc', 'E&TC Engineering'),
        ('inst', 'Instrumental Engineering'),
        ('prod', 'Production Engineering'),
    )
    sem_choices = (('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'))
    year_choices = (('F.E', 'F.E'), ('S.E', 'S.E'), ('T.E', 'T.E'), ('B.E', 'B.E'))

    code = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    dept = models.CharField(max_length=50, choices=dept_choices)
    year = models.CharField(max_length=3, choices=year_choices)
    sem = models.CharField(max_length=1, choices=sem_choices)

    def __str__(self):
        return self.code + " " + self.name


class Subjects(models.Model):
    div_choices = (('A', 'A'), ('B', 'B'))

    subject_name = models.ForeignKey(Subject, on_delete=False, to_field='name')
    division = models.CharField(max_length=2, choices=div_choices)

    class Meta:
        abstract = True


class Labs(models.Model):
    batch_choices = (
        ('A1', 'A1'), ('A2', 'A2'), ('A3', 'A3'), ('A4', 'A4'),
        ('B1', 'B1'), ('B2', 'B2'), ('B3', 'B3'), ('B4', 'B4'),
    )

    lab_name = models.ForeignKey(Lab, on_delete=False, to_field='name')
    batch = models.CharField(max_length=3, choices=batch_choices)

    class Meta:
        abstract = True


class Teacher(models.Model):
    year_choices = (('N/A', 'N/A'),('F.E', 'F.E'), ('S.E', 'S.E'), ('T.E', 'T.E'), ('B.E', 'B.E'))
    dept_choices = (
        ('comp', 'Computer Engineering'),
        ('civil', 'Civil Engineering'),
        ('mech', 'Mechanical Engineering'),
        ('it', 'Information Technology Engineering'),
        ('e&tc', 'E&TC Engineering'),
        ('inst', 'Instrumental Engineering'),
        ('prod', 'Production Engineering'),
    )

    name = models.CharField(max_length=80, unique=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=50, primary_key=True)
    email_id = models.CharField(max_length=50)
    primary_phone_no = models.CharField(max_length=10)
    secondary_phone_no = models.CharField(max_length=10)
    cc = models.CharField(max_length=3, choices=year_choices, default='None')
    department = models.CharField(max_length=50, choices=dept_choices)
    subjects = models.ArrayModelField(model_container=Subjects)
    labs = models.ArrayModelField(model_container=Labs)

    def __str__(self):
        return self.name


class Student(models.Model):
    # choice tuples
    year_choices = (('F.E', 'F.E'), ('S.E', 'S.E'), ('T.E', 'T.E'), ('B.E', 'B.E'))
    batch_choices = (
        ('A1', 'A1'), ('A2', 'A2'), ('A3', 'A3'), ('A4', 'A4'),
        ('B1', 'B1'), ('B2', 'B2'), ('B3', 'B3'), ('B4', 'B4'),
    )
    dept_choices = (
        ('comp', 'Computer Engineering'),
        ('civil', 'Civil Engineering'),
        ('mech', 'Mechanical Engineering'),
        ('it', 'Information Technology Engineering'),
        ('e&tc', 'E&TC Engineering'),
        ('inst', 'Instrumental Engineering'),
        ('prod', 'Production Engineering'),
    )
    div_choices = (('A', 'A'), ('B', 'B'))
    # data model
    roll_no = models.CharField(max_length=12, blank=False, primary_key=True, null=False)
    name = models.CharField(max_length=100)
    department = models.CharField(max_length=10, choices=dept_choices, default='comp')
    division = models.CharField(max_length=2, choices=div_choices)
    year = models.CharField(max_length=3, choices=year_choices, default='fe')
    batch = models.CharField(max_length=2, choices=batch_choices, default='a1')
    teacher_guardian = models.ForeignKey(Teacher, on_delete=False, to_field='name')
    email_id = models.EmailField(max_length=100)
    primary_phone_no = models.CharField(max_length=10)
    parents_phone_no = models.CharField(max_length=10)

    def __str__(self):
        return self.name
