from rest_framework import generics, permissions, status
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from .models import Categories, FAQs, Products
from .serializers import (
    CategoriesSerializer, 
    FAQsSerializer, 
    ProductsSerializer, 
    ProductDetailsSerializer, 
    ContactFormSerializer
)
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

class Home(APIView):
    def get(self, request):
        return Response({'message': 'Hello, World!'})

class FAQsCreateView(generics.CreateAPIView):
    queryset = FAQs.objects.all()
    # serializer_class = FAQsSerializer
    # permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['post']

class FAQsListView(generics.ListAPIView):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]
    
    queryset = FAQs.objects.all()
    serializer_class = FAQsSerializer
    http_method_names = ['get']

class CategoriesView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def get(self, request):
        categories = Categories.objects.all()
        serializer = CategoriesSerializer(categories, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CategoriesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductsView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def get(self, request):
        products = Products.objects.all()
        serializer = ProductsSerializer(products, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProductsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductDetailsView(generics.RetrieveAPIView):
    queryset = Products.objects.all()
    serializer_class = ProductDetailsSerializer
    lookup_field = 'id'

class SubmitContactFormView(APIView):
    def post(self, request):
        serializer = ContactFormSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Form submitted successfully!'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
