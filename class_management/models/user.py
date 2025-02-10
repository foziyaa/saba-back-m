from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid

class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    role = models.CharField(
        max_length=50,
        choices=[
            ('student', 'Student'),
            ('teacher', 'Teacher'),
            ('department_head', 'Department Head'),
            ('program_office', 'Program Office'),
            ('registrar', 'Registrar'),
            ('super_admin', 'Super Admin'),
        ]
    )
    phone = models.CharField(max_length=20, blank=True, null = True)
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='class_management_user_groups',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='class_management_user_permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    def __str__(self):
        return self.username

    @staticmethod
    def get_available_roles():
       return [choice[0] for choice in User._meta.get_field('role').choices]