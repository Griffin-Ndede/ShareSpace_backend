from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from .models import Listing
from .serializers import ListingSerializer
from django.shortcuts import get_object_or_404

# Create your views here.

class ListingView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def get(self, request):
        listing = Listing.objects.all()
        serializer = ListingSerializer(listing, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ListingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ListingDetailView(APIView):

    def get(self, request, id):
        listing = get_object_or_404(Listing, id=id)
        serializer = ListingSerializer(listing)
        return Response(serializer.data)