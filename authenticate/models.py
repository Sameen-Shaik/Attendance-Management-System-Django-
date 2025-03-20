from django.db import models
from django.contrib.auth.models import AbstractUser

class MyUser(AbstractUser):
    STUDENT = 'student'
    FACULTY = 'faculty'

    USER_TYPES = [
        (STUDENT, "Student"),
        (FACULTY, "Faculty")
    ]

    user_type = models.CharField(max_length=10, choices=USER_TYPES, default=STUDENT)
    username = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    joined = models.DateField(null=True, blank=True)
    department = models.CharField(max_length=3, blank=True, null=True)

    groups = models.ManyToManyField('auth.Group', related_name='myuser_set', blank=True)
    user_permissions = models.ManyToManyField('auth.Permission', related_name='myuser_permissions', blank=True)

    def __str__(self):
        return f"{self.name} ({self.user_type}) {self.username} {self.department} {self.joined} {self.email}"


class Student(models.Model):
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE, primary_key=True)
    def __str__(self):
        return f"Student: {self.user.name} ({self.user.username})"


class Faculty(models.Model):
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE, primary_key=True)
    def __str__(self):
        return f"Faculty: {self.user.name} ({self.user.username})"