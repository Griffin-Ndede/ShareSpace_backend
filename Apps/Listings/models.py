from django.db import models
from django.contrib.auth import get_user_model
import cloudinary
from cloudinary.models import CloudinaryField

User = get_user_model()


# Create your models here.
class Listing(models.Model):
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="listings", null=True
    )
    category = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = CloudinaryField('products', null=True)
    startDate = models.DateField(null=True)
    endDate = models.DateField(null=True)
    condition = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    deposit = models.CharField(max_length=255, null=True)
    accessories = models.CharField(max_length=255, null=True)
    # name = models.CharField(max_length=255)
    # phoneNumber = models.IntegerField(null=True)
    # emailAddress = models.CharField(max_length=255, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.title
