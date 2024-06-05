from rest_framework import serializers
from .models import FAQs

class FAQsSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQs
        fields = '__all__'
        
        #convenient way to include all the fields without explicitly listing them 
        # alternatively to represent a subset of the model fields we could use a tuple we could list them as 
        # fields = ('Question', 'Answer')