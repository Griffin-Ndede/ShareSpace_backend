from django.contrib import admin
from .models import Categories, FAQs, Products
# Register your models here.

admin.site.register(Categories)
admin.site.register(FAQs)
admin.site.register(Products)