from django.contrib import admin
from .models import Listing, ListingModerationEvent, Notification, RentalRequest

# Register your models here.
admin.site.register(Listing)
admin.site.register(Notification)
admin.site.register(RentalRequest)
admin.site.register(ListingModerationEvent)