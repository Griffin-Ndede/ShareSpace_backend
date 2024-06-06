from rest_framework import generics, permissions
from .models import Categories, FAQs
from .serializers import CategoriesSerializer, FAQsSerializer


class FAQsCreateView(generics.CreateAPIView):
    queryset = FAQs.objects.all()
    serializer_class = FAQsSerializer
    # permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['post']

class FAQsListView(generics.ListAPIView):
    queryset = FAQs.objects.all()
    serializer_class = FAQsSerializer
    http_method_names = ['get']

class CategoriesCreateView(generics.CreateAPIView):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    http_method_names = ['post']

class CategoriesListView(generics.ListAPIView):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    http_method_names = ['get']
    