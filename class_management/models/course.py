
from django.db import models
import uuid
from class_management.models.user import User
from class_management.models.department import Department

class Course(models.Model):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  name = models.CharField(max_length=255)
  course_code = models.CharField(max_length=50, unique=True)
  year = models.IntegerField()
  semester = models.IntegerField()
  department = models.ForeignKey(Department, on_delete=models.CASCADE)
  teacher = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, limit_choices_to={'role': 'teacher'})
  isActive = models.BooleanField(default=True) # Added this

  def __str__(self):
      return f"{self.name} ({self.course_code})"