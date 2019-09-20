from django.contrib import admin
from .models import Teacher, Student, Subject, Lab
# Register your models here.
admin.site.register(Teacher)
admin.site.register(Student)
admin.site.register(Subject)
admin.site.register(Lab)
