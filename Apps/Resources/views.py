from rest_framework import status
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from .models import Category, FAQ, Product
from .serializers import (
    CategoriesSerializer, 
    FAQsSerializer, 
    # ProductsSerializer,
    # ProductDetailsSerializer, 
    ContactFormSerializer
)

class Home(APIView):
    def get(self, request):
        return Response({'message': 'Hello, World!'})

class FAQsCreateView(APIView):
    def post(self, request):
        serializer = FAQsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FAQsListView(APIView):
    def get(self, request):
        faqs = FAQ.objects.all()
        serializer = FAQsSerializer(faqs, many=True)
        return Response(serializer.data)

class CategoriesView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def get(self, request):
        categories = Category.objects.all()
        serializer = CategoriesSerializer(categories, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CategoriesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class ProductsView(APIView):
#     parser_classes = (MultiPartParser, FormParser)

#     def get(self, request):
#         products = Product.objects.all()
#         serializer = ProductsSerializer(products, many=True)
#         return Response(serializer.data)

#     def post(self, request):
#         serializer = ProductsSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class ProductDetailsView(APIView):
#     def get(self, request, id):
#         product = get_object_or_404(Product, id=id)
#         serializer = ProductDetailsSerializer(product)
#         return Response(serializer.data)

class SubmitContactFormView(APIView):
    def post(self, request):
        serializer = ContactFormSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Form submitted successfully!'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

