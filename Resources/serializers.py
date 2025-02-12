from rest_framework import serializers
from .models import Categories, FAQs, Products, ProductImage, ContactForm1, User


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
    class Meta:
        models= User
        fields = "__all__"