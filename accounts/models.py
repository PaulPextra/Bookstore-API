from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

class CustomUser(AbstractUser):
    """Extending our user model"""
    id = models.UUIDField(primary_key=True, unique=True, editable=False, default=uuid.uuid4)
    phone = models.CharField(max_length=20, blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True, null=True)
    address = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return self.username