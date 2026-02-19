from django.contrib import admin
from .models import Listing, Notification

# Register your models here.
admin.site.register(Listing)
admin.site.register(Notification)