from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    ROLE_CHOICES = [
        ("renter", "Renter"),
        ("owner", "Owner"),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="renter")



