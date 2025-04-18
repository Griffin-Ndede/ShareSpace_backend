from django.db import models
from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
import os

# Validators
@deconstructible
class ValidateImageFileExtension:
    valid_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff']

    def __call__(self, value):
        ext = os.path.splitext(value.name)[1]
        if ext.lower() not in self.valid_extensions:
            raise ValidationError(f'Unsupported file extension. Supported extensions are: {", ".join(self.valid_extensions)}')

# File upload paths
def upload_to(instance, filename):
    if isinstance(instance, Category):
        return f'category_images/{filename}'
    elif isinstance(instance, ProductImage):
        return f'product_images/{filename}'
    return f'uploads/{filename}'

# Models
class FAQ(models.Model):
    title = models.CharField(max_length=300)
    answer = models.TextField()

    def __str__(self):
        return self.title

class Category(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to=upload_to, null=True, validators=[ValidateImageFileExtension()])

    def __str__(self):
        return self.title

class Product(models.Model):
    category = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    description = models.TextField()
    startDate = models.DateField(null=True)
    endDate = models.DateField(null=True)
    condition = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    deposit = models.CharField(max_length=255, null=True)
    accessories = models.CharField(max_length=255, null=True)
    name = models.CharField(max_length=255)
    phoneNumber = models.IntegerField(null=True)
    emailAddress = models.CharField(max_length=255, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.title

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField(upload_to=upload_to, validators=[ValidateImageFileExtension()])

    def __str__(self):
        return f"Image for {self.product.title}"

class ContactForm1(models.Model):
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    phone = models.IntegerField()
    item = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    startDate = models.DateField()
    endDate = models.DateField()

    def __str__(self):
        return self.name

class User(models.Model):
    username = models.CharField(max_length=200)
    firstname = models.CharField(max_length=200)
    lastname = models.CharField(max_length=200)
    email =models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    password2 = models.CharField(max_length=200)

    def __str__(self):
        return self.username
