from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid

class Department(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    role = models.CharField(max_length=50, choices=[
        ('student', 'Student'),
        ('teacher', 'Teacher'),
        ('department_head', 'Department Head'),
        ('program_office', 'Program Office'),
        ('registrar', 'Registrar'),
        ('super_admin', 'Super Admin')
    ])
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        
        return self.username

# class_management/models/semester_schedule.py
    
from class_management.models.user import User
from class_management.models.department import Department


class SemesterSchedule(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    semester = models.CharField(max_length=255) # Added Semester Field
    section = models.CharField(max_length=50)
    subject = models.TextField()
    teacher = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, limit_choices_to={'role': 'teacher'})
    day_of_week = models.CharField(
        max_length=20,
        choices=[
            ('Monday', 'Monday'),
            ('Tuesday', 'Tuesday'),
            ('Wednesday', 'Wednesday'),
            ('Thursday', 'Thursday'),
            ('Friday', 'Friday'),
            ('Saturday', 'Saturday'),
            ('Sunday', 'Sunday'),
        ]
    )
    period = models.CharField(max_length=100)
    details = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    def __str__(self):
     return f"{self.subject} - {self.section} - {self.day_of_week}"
