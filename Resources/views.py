from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from .models import Categories, FAQs, Products
from .serializers import CategoriesSerializer, FAQsSerializer, ProductsSerializer


class FAQsCreateView(generics.CreateAPIView):
    queryset = FAQs.objects.all()
    serializer_class = FAQsSerializer
    # permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['post']

class FAQsListView(generics.ListAPIView):
    queryset = FAQs.objects.all()
    serializer_class = FAQsSerializer
    http_method_names = ['get']

class CategoriesView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def get(self, request, *args, **kwargs):
        categories = Categories.objects.all()
        serializer = CategoriesSerializer(categories, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        Categoriess_serializer = CategoriesSerializer(data=request.data)
        if Categoriess_serializer.is_valid():
            Categoriess_serializer.save()
            return Response(Categoriess_serializer.data, status=status.HTTP_201_CREATED)
        else:
            print('error', Categoriess_serializer.errors)
            return Response(Categoriess_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class ProductsView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def get(self, request, *args, **kwargs):
        products = Products.objects.all()
        serializer = ProductsSerializer(products, many= True)
        return Response(serializer.data)
    
    def post(self, request, *args, **kwargs):
        Products_serializer = ProductsSerializer(data=request.data)
        if Products_serializer.is_valid():
            Products_serializer.save()
            return Response(Products_serializer.data, status= status.HTTP_201_CREATED)
        else:
            print('error', Products_serializer.errors)
            return Response(Products_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        