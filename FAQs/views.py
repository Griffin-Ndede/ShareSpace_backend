from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import generics, permissions
from .models import FAQs
from .serializers import FAQsSerializer


class FAQsCreateView(generics.CreateAPIView):
    queryset = FAQs.objects.all()
    serializer_class = FAQsSerializer
    # permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['post']

class FAQsListView(generics.ListAPIView):
    queryset = FAQs.objects.all()
    serializer_class = FAQsSerializer
    http_method_names = ['get']