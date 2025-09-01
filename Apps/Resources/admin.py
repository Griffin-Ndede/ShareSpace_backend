from django.contrib import admin
from .models import Category, FAQ, Product
# Register your models here.

admin.site.register(Category)
admin.site.register(FAQ)
admin.site.register(Product)