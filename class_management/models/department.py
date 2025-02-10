from django.db import models
import uuid

class Department(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)  # Added is_active field

    def __str__(self):
        return self.name