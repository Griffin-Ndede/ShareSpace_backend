from rest_framework import serializers
from .models import Categories, FAQs, Products, ContactForm1


class FAQsSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQs
        fields = '__all__'

class CategoriesSerializer(serializers.ModelSerializer):
    image_url = serializers.ImageField(required=False)

    class Meta:
        model = Categories
        fields ="__all__"

class ProductsSerializer(serializers.ModelSerializer):
    photos_url = serializers.ImageField(required =False)
    
    class Meta:
        model = Products
        fields = "__all__"

class ProductDetailsSerializer(serializers.ModelSerializer):
    photos_url = serializers.ImageField(required=False)

    class Meta:
        model = Products
        fields = "__all__"

class ContactFormSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ContactForm1
        fields = "__all__"