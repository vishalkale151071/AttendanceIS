from djongo import models

class Attendance(models.Model):
    roll_no = models.CharField(max_length=10)
    status = models.CharField(max_length=1, default='P')
    class Meta:
        abstract = True


class AttendanceSubject(models.Model):
    date = models.DateField()
    from_time = models.TimeField()
    to_time = models.TimeField()
    subject = models.CharField(max_length=10)
    div = models.CharField(max_length=5)
    slots = models.IntegerField()
    attendance = models.ArrayModelField(model_container=Attendance)


class AttendanceLab(models.Model):
    date = models.DateField()
    from_time = models.TimeField()
    to_time = models.TimeField()
    lab = models.CharField(max_length=10)
    batch = models.CharField(max_length=5)
    attendance = models.ArrayModelField(model_container=Attendance)