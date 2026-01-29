from rest_framework import serializers
from .models import User, UserProfile


class UserProfileSerializer(serializers.Serializer):
    """
    serializer for a profile that is tied to a user
    """
class Meta:
    model= UserProfile
    fields = ["username", "first_name", "last_name", "email", "phone_number" ,"profile_photo", "bio"]

class UserSerializer(serializers.ModelSerializer):
    # Nest the UserProfileSerializer to handle user profile data together with the user
    profile = UserProfileSerializer(read_only=True) 

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'profile', 'is_superuser', 'is_staff']
