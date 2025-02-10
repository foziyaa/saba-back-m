# class_management/models/academic_calendar.py

from django.db import models
import uuid

class AcademicCalendar(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date = models.DateField()
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return f"{self.name} - {self.date}"