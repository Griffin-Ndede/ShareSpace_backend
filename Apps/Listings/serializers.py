from rest_framework import serializers
from .models import Listing, User

class OwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', "first_name", "last_name"] 
        # fields = "__all__"
class ListingSerializer(serializers.ModelSerializer):
    owner = OwnerSerializer(read_only=True)
    class Meta:
        model = Listing
        fields = "__all__"