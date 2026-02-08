from rest_framework import serializers
from .models import Category, FAQ, Product, ProductImage, ContactForm1


class FAQsSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = '__all__'


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image']  # Include the necessary fields


# class ProductsSerializer(serializers.ModelSerializer):
#     photos = ProductImageSerializer(many=True, read_only=True)  # Nested serializer for photos

#     class Meta:
#         model = Product
#         fields = "__all__"


# class ProductDetailsSerializer(serializers.ModelSerializer):
#     photos = ProductImageSerializer(many=True, read_only=True)  # Nested serializer for photos

#     class Meta:
#         model = Product
#         fields = "__all__"


class ContactFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactForm1
        fields = "__all__"

