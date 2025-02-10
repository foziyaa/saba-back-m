
from django.db import models
import uuid
from class_management.models import User, Department
class Notification(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    message = models.TextField()
    type = models.CharField(max_length=50, choices=[
        ('announcement', 'Announcement'),
        ('reminder', 'Reminder'),
        ('alert', 'Alert')
    ])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user if self.user else self.department}"
