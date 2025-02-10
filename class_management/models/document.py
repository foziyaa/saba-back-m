from django.db import models
import uuid
class Document(models.Model):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  title = models.CharField(max_length=255)
  description = models.TextField()
  image = models.ImageField(upload_to='documents/', blank=True, null=True) 
  uploaded_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return self.title