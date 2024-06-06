from rest_framework import serializers
from .models import Categories, FAQs


class FAQsSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQs
        fields = '__all__'

class CategoriesSerializer(serializers.ModelSerializer):
    image_url = serializers.ImageField(required=False)

    class Meta:
        model = Categories
        fields = ['id', 'title', 'image_url']