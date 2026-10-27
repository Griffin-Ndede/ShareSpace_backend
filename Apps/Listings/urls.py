
from django.urls import path
from .views import (
    ListingView,
    ListingDetailView,
    MyListingsView,
    ListingModerationView,
    NotificationView,
    RentalRequestView,
    MarkNotificationReadView,
)

urlpatterns = [
    path("listing/", ListingView.as_view(), name="listing"),
    path("listing/<int:id>/", ListingDetailView.as_view(), name="listing-detail"),

    path("my-listings/", MyListingsView.as_view(), name="my-listings"),
    path("my-listings/<int:id>/", MyListingsView.as_view(), name="my-listing-detail"),

    path("admin/listings/", ListingModerationView.as_view(), name="listing-moderation-queue"),
    path("admin/listings/<int:id>/moderate/", ListingModerationView.as_view(), name="listing-moderate"),

    path("request/<int:id>/", RentalRequestView.as_view(), name="rental-request"),
    path("notifications/", NotificationView.as_view(), name="notifications"),
    path("notifications/<int:id>/read/", MarkNotificationReadView.as_view(), name="mark-notification-read"),
]
