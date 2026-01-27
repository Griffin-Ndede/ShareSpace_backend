from rest_framework import serializers
from .models import User, UserProfile
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model

User = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for registering a new user.
    """

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "password"]

    def validate_password(self, value):
        return make_password(value)  # Hash the password

    def create(self, validated_data):
        return User.objects.create(**validated_data)


class UserLoginSerializer(serializers.Serializer):
    """
    Serializer for user login.
    """

    username = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True)


class UserProfileSerializer(serializers.Serializer):
    """
    serializer for a profile that is tied to a user
    """
class Meta:
    model= UserProfile
    fields = ["username", "first_name", "last_name", "email", "phone_number" ,"profile_photo", "bio"]

class UserSerializer(serializers.ModelSerializer):
    # Nest the UserProfileSerializer to handle user profile data together with the user
    profile = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'profile', 'is_superuser', 'is_staff']
