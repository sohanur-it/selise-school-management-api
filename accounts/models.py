from django.db import models
# from django.db.models.signals import post_save
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserManger(BaseUserManager):
    def create_user(self, email, is_student, is_teacher, password=None):
        if not email:
            raise ValueError('User must have an email')
        user = self.model(
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.is_student = is_student
        user.is_teacher = is_teacher
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, is_student, is_teacher, password=None):
        user = self.create_user(email=email, is_student=is_student, is_teacher=is_teacher, password=password)
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(email=email, is_student=False, is_teacher=False,
                                password=password)
        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(verbose_name='email', max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)

    def __str__(self):
        return self.email

    objects = UserManger()
    USERNAME_FIELD = 'email'

    def __str__(self):
        return "{}".format(self.email)

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True


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
