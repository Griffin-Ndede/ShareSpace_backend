from django.db import models
from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
import os
from PIL import Image

# Create your models here.
class FAQs(models.Model):
    title = models.CharField(max_length=300)
    answer = models.TextField()

    def __str__(self):
        return self.title

def upload_to(instance, filename):
    # Determine the path based on the model class
    if isinstance(instance, Categories):
        return f'category_images/{filename}'
    elif isinstance(instance, Products):
        return f'product_images/{filename}'
    return f'uploads/{filename}'

@deconstructible
class ValidateImageFileExtension(object):
    valid_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff']

    def __call__(self, value):
        ext = os.path.splitext(value.name)[1]
        if ext.lower() not in self.valid_extensions:
            raise ValidationError(f'Unsupported file extension. Supported extensions are: {", ".join(self.valid_extensions)}')


class Categories(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to=upload_to, null=True, validators=[ValidateImageFileExtension()])
    
    def __str__(self):
        return self.title
    
class Products(models.Model):
    category = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    description = models.TextField()
    photos = models.ImageField(upload_to=upload_to, null=True, validators=[ValidateImageFileExtension()])
    startDate = models.DateField(max_length=200, null=True)
    endDate = models.DateField(max_length=200, null=True)
    condition = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    deposit = models.CharField(max_length=255, null=True)
    accessories = models.CharField(max_length=255, null=True)
    name= models.CharField(max_length=255)
    phoneNumber = models.IntegerField(null=True)
    emailAddress  = models.CharField(max_length=255, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.title

class ContactForm1(models.Model):
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    phone = models.IntegerField()
    item = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    startDate = models.DateField(max_length=200)
    endDate = models.DateField(max_length=200)

    def __str__(self):
        return self.name