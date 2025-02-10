from django.db import models
import uuid
from class_management.models.user import User
from class_management.models.department import Department
from class_management.models import Course #Add

class SemesterSchedule(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    semester = models.CharField(max_length=255) # Added Semester Field
    section = models.CharField(max_length=50)
    subject = models.TextField()
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, blank=True) # Add the attribute to specify relation

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
    classroom_number = models.CharField(max_length=50, blank=True, null=True) #Add this line
    start_time = models.CharField(max_length=50, blank=True, null = True) #Add this line
    end_time = models.CharField(max_length=50, blank=True, null = True) #Add this line

    def __str__(self):
        return f"{self.subject} - {self.section} - {self.day_of_week}"