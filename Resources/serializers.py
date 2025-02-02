from rest_framework import serializers
from .models import Categories, FAQs, Products, ProductImage, ContactForm1
from django.contrib.auth.models import User



class FAQsSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQs
        fields = '__all__'


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = "__all__"


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image']  # Include the necessary fields


class ProductsSerializer(serializers.ModelSerializer):
    photos = ProductImageSerializer(many=True, read_only=True)  # Nested serializer for photos

    class Meta:
        model = Products
        fields = "__all__"


class ProductDetailsSerializer(serializers.ModelSerializer):
    photos = ProductImageSerializer(many=True, read_only=True)  # Nested serializer for photos

    class Meta:
        model = Products
        fields = "__all__"


class ContactFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactForm1
        fields = "__all__"

class UserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password', 'password2')
        extra_kwargs = {
            'password': {'write_only': True},
        }
    
    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({"password2": "Passwords must match."})
        return data

    def create(self, validated_data):
        validated_data.pop('password2')  # Remove password2 field
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )
        return user