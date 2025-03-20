from django.db import models
from authenticate.models import Student, Faculty
import uuid


# Create your models here.

class Course(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    department = models.CharField(max_length=3)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.code} - {self.name}"


class CourseBatch(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    faculty = models.ManyToManyField(Faculty, blank=True)
    students = models.ManyToManyField(Student, blank=True)
    term = models.CharField(max_length=12, verbose_name="Batch and Term", help_text="Eg: 22 - Term -1")  # e.g., "Fall 2023"
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"{self.course.code} -{self.course.name} {self.term}"


class Session(models.Model):
    session_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    course_batch = models.ForeignKey(CourseBatch, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    topic = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.course_batch} - {self.date}"


class Attendance(models.Model):
    STATUS_CHOICES = [
        ('present', 'Present'),
        ('absent', 'Absent'),
    ]

    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='present')
    timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['session', 'student']
        # verbose_name_plural = 'Attendance Records'

    def __str__(self):
        return f"{self.student.user.username} - {self.status} - {self.session.date}" 

