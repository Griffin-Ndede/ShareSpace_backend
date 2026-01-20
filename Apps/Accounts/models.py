from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    # Add custom fields if needed
    pass

class UserProfile(models.Model):
    phone_number = models.CharField(max_length=15, blank=True)
