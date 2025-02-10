from django.db import models
import uuid
from class_management.models import User, Course
class Attendance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="student_attendances", null=True, blank = True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=20, choices=[
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('late', 'Late')
    ])
    recorded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="recorded_attendance")

    def __str__(self):
        return f"{self.user.username if self.user else 'N/A'} - {self.course.name} - {self.status}"