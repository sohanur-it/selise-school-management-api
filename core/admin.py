from django.contrib import admin

# Register your models here.
from .models import Teacher, Student, ClassSchedule

admin.site.register(Teacher)
admin.site.register(Student)
admin.site.register(ClassSchedule)