from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.response import Response
from rest_framework import status
from .models import Listing, Notification
from .serializers import (
    ListingSerializer,
    NotificationSerializer,
    myListingsSerializer,
    RentalRequestSerializer,
)
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

# Create your views here.


class ListingView(APIView):
    parser_classes = (MultiPartParser, JSONParser)
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get(self, request):
        listing = Listing.objects.all()
        serializer = ListingSerializer(listing, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ListingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListingDetailView(APIView):

    def get(self, request, id):
        listing = get_object_or_404(Listing, id=id)
        serializer = ListingSerializer(listing)
        return Response(serializer.data)


class myListingsView(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        listings = Listing.objects.filter(owner=request.user)
        serializer = myListingsSerializer(listings, many=True)
        return Response(serializer.data)

    def delete(self, request, id):
        listing = get_object_or_404(Listing, id=id, owner=request.user)
        listing.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class RentalRequestView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        listing = get_object_or_404(Listing, id=id)

        serializer = RentalRequestSerializer(data=request.data)
        if serializer.is_valid():
            rental_request = serializer.save(
                renter=request.user,
                owner=listing.owner,
                listing=listing
            )

            Notification.objects.create(
                user=listing.owner,
                title="New rental request",
                message=f"{request.user.username} requested your item: {listing.title}",
                link=f"/checkout/{listing.id}",
            )

            return Response(
                RentalRequestSerializer(rental_request).data,
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class NotificationView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        notifications = Notification.objects.filter(user=request.user).order_by("-created_at")
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class MarkNotificationReadView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def patch(self, request, id):
        notification = get_object_or_404(Notification, id=id, user=request.user)
        notification.is_read = True
        notification.save()
        return Response({"message": "Marked as read"}, status=status.HTTP_200_OK)


