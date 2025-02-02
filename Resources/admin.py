from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Categories, FAQs, Products, User


# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Categories)
admin.site.register(FAQs)
admin.site.register(Products)