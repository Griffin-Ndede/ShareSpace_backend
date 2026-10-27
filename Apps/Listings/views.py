
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.utils import timezone

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import (
    Listing,
    Notification,
    RentalRequest,
    ListingModerationEvent,
)
from .serializers import (
    ListingSerializer,
    NotificationSerializer,
    myListingsSerializer,
    RentalRequestSerializer,
)


class ListingView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def get(self, request):
        # Public marketplace results must only include approved listings.
        listings = Listing.objects.filter(status="approved")
        serializer = ListingSerializer(listings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ListingSerializer(data=request.data)

        if serializer.is_valid():
            listing = serializer.save(
                owner=request.user,
                status="pending_review",
                review_notes="",
                reviewed_by=None,
                reviewed_at=None,
            )

            user = request.user
            if user.role != "owner":
                user.role = "owner"
                user.save(update_fields=["role"])

            return Response(
                ListingSerializer(listing).data,
                status=status.HTTP_201_CREATED,
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )


class ListingDetailView(APIView):
    # Approved listings can be viewed publicly.
    # Owners and staff can also view listings that are under review.
    def get(self, request, id):
        listing = get_object_or_404(Listing, id=id)

        is_owner = (
            request.user.is_authenticated
            and listing.owner_id == request.user.id
        )
        is_admin = (
            request.user.is_authenticated
            and request.user.is_staff
        )

        if listing.status != "approved" and not (is_owner or is_admin):
            return Response(
                {"detail": "Listing not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        return Response(ListingSerializer(listing).data)


class MyListingsView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def get(self, request):
        listings = Listing.objects.filter(owner=request.user)
        serializer = myListingsSerializer(listings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, id):
        listing = get_object_or_404(
            Listing,
            id=id,
            owner=request.user,
        )

        serializer = ListingSerializer(
            listing,
            data=request.data,
            partial=True,
        )

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

        with transaction.atomic():
            # Any edit requires the listing to be reviewed again.
            listing = serializer.save(
                status="pending_review",
                review_notes="",
                reviewed_by=None,
                reviewed_at=None,
            )

            ListingModerationEvent.objects.create(
                listing=listing,
                moderator=None,
                action="resubmitted",
                notes="Listing edited and resubmitted for review.",
            )

        return Response(
            myListingsSerializer(listing).data,
            status=status.HTTP_200_OK,
        )

    def delete(self, request, id):
        listing = get_object_or_404(
            Listing,
            id=id,
            owner=request.user,
        )
        listing.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ListingModerationView(APIView):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        # Staff can filter the moderation queue using ?status=pending_review
        listing_status = request.query_params.get(
            "status",
            "pending_review",
        )

        valid_statuses = {
            "pending_review",
            "changes_requested",
            "approved",
            "rejected",
        }

        if listing_status not in valid_statuses:
            return Response(
                {"detail": "Invalid listing status filter."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        listings = Listing.objects.filter(
            status=listing_status
        ).order_by("created_at")

        return Response(
            ListingSerializer(listings, many=True).data,
            status=status.HTTP_200_OK,
        )

    def post(self, request, id):
        listing = get_object_or_404(Listing, id=id)

        action = request.data.get("action")
        notes = request.data.get("notes", "")

        action_to_status = {
            "approve": "approved",
            "reject": "rejected",
            "request_changes": "changes_requested",
        }

        if action not in action_to_status:
            return Response(
                {
                    "detail": (
                        "Action must be approve, reject, "
                        "or request_changes."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not isinstance(notes, str):
            return Response(
                {"notes": "Notes must be text."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if action in {"reject", "request_changes"} and not notes.strip():
            return Response(
                {
                    "notes": (
                        "Provide an explanation when rejecting "
                        "a listing or requesting changes."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        new_status = action_to_status[action]

        with transaction.atomic():
            listing.status = new_status
            listing.review_notes = notes.strip()
            listing.reviewed_by = request.user
            listing.reviewed_at = timezone.now()

            listing.save(
                update_fields=[
                    "status",
                    "review_notes",
                    "reviewed_by",
                    "reviewed_at",
                    "updated_at",
                ]
            )

            event_action = {
                "approve": "approved",
                "reject": "rejected",
                "request_changes": "changes_requested",
            }[action]

            ListingModerationEvent.objects.create(
                listing=listing,
                moderator=request.user,
                action=event_action,
                notes=notes.strip(),
            )

            Notification.objects.create(
                user=listing.owner,
                title={
                    "approve": "Listing approved",
                    "reject": "Listing rejected",
                    "request_changes": "Changes requested for your listing",
                }[action],
                message={
                    "approve": (
                        f'Your listing "{listing.title}" has been approved.'
                    ),
                    "reject": (
                        f'Your listing "{listing.title}" was rejected. '
                        f"Reason: {notes.strip()}"
                    ),
                    "request_changes": (
                        f'Changes are required for "{listing.title}". '
                        f"Notes: {notes.strip()}"
                    ),
                }[action],
                link=f"/my-listings/{listing.id}",
            )

        return Response(
            ListingSerializer(listing).data,
            status=status.HTTP_200_OK,
        )


class RentalRequestView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        listing = get_object_or_404(
            Listing,
            id=id,
            status="approved",
        )

        if listing.owner_id == request.user.id:
            return Response(
                {"detail": "You cannot request to rent your own listing."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = RentalRequestSerializer(data=request.data)

        if serializer.is_valid():
            rental_request = serializer.save(
                renter=request.user,
                owner=listing.owner,
                listing=listing,
            )

            Notification.objects.create(
                user=listing.owner,
                title="New rental request",
                message=(
                    f"{request.user.username} requested your item: "
                    f"{listing.title}"
                ),
                link=f"/checkout/{listing.id}",
            )

            return Response(
                RentalRequestSerializer(rental_request).data,
                status=status.HTTP_201_CREATED,
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )


class NotificationView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        notifications = Notification.objects.filter(
            user=request.user
        ).order_by("-created_at")

        serializer = NotificationSerializer(
            notifications,
            many=True,
        )

        return Response(serializer.data, status=status.HTTP_200_OK)


class MarkNotificationReadView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def patch(self, request, id):
        notification = get_object_or_404(
            Notification,
            id=id,
            user=request.user,
        )

        notification.is_read = True
        notification.save(update_fields=["is_read"])

        return Response(
            {"message": "Marked as read"},
            status=status.HTTP_200_OK,
        )
