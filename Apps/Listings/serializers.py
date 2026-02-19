from rest_framework import serializers
from .models import Listing, Notification, RentalRequest, User
class OwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name"]


class ListingSerializer(serializers.ModelSerializer):
    owner = OwnerSerializer(read_only=True)
    class Meta:
        model = Listing
        fields = "__all__"
        read_only_fields = ["owner"]
class myListingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Listing
        fields = "__all__"

class RentalRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = RentalRequest
        fields = ['id', 'listing', 'renter', 'owner', 'start_date', 'end_date', 'status', 'created_at']
        read_only_fields = ['renter',"listing", 'owner', 'status', 'created_at']

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = "__all__"
