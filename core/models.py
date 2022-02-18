from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


# Create your models here.

class Organisation(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name


martial_choices = (
    ('MARRIED', 'MARRIED'),
    ('UNMARRIED', 'UNMARRIED')
)


# Create your models here.
class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='teacher')
    first_name = models.CharField(max_length=20, blank=True, null=True)
    last_name = models.CharField(max_length=20, blank=True, null=True)
    nid_no = models.CharField(max_length=100, blank=True, null=True)
    martial_status = models.CharField(max_length=20, choices=martial_choices, default='UNMARRIED')
    birthdate = models.DateField(auto_now=False, null=True, blank=True)
    joining_date = models.DateField(auto_now=False, null=True, blank=True)

    objects = models.Manager()

    def __str__(self):
        return str(self.pk) + '-' + str(self.user)


class ClassSchedule(models.Model):
    class_name = models.CharField(max_length=255)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    start_time = models.TimeField()
    end_time = models.TimeField()


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student')
    first_name = models.CharField(max_length=20, blank=True, null=True)
    last_name = models.CharField(max_length=20, blank=True, null=True)
    nid_no = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=100, blank=True, null=True)
    birthdate = models.DateField(auto_now=False, null=True, blank=True)

    objects = models.Manager()

    def __str__(self):
        return str(self.pk) + '-' + str(self.user)
