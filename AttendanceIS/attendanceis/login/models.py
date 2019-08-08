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
    #id is employee number of a teacher
    id = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=80)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    email_id = models.CharField(max_length=50)
    primary_phone_no = models.CharField(max_length=10)
    secondary_phone_no = models.CharField(max_length=10)
    tg = models.CharField(max_length=1, default='1')
    cc = models.CharField(max_length=1, default='0')
    subjects = models.ArrayModelField(model_container=Subjects)
    labs = models.ArrayModelField(model_container=Lab)
