from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    is_renter = models.BooleanField(default=True)
    is_lister = models.BooleanField(default=False)



