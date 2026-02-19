from django.urls import path
from .views import (
    ListingView,
    ListingDetailView,
    myListingsView,
    NotificationView,
    RentalRequestView,
    MarkNotificationReadView
)

urlpatterns = [
    path("listing/", ListingView.as_view(), name="listing"),
    path("listing/<int:id>/", ListingDetailView.as_view(), name="listing-detail"),
    path("my-listings/", myListingsView.as_view(), name="my-listings"),
    path("my-listings/<int:id>/", myListingsView.as_view(), name="my-listing-delete"),
    path("request/<int:id>/", RentalRequestView.as_view(), name="rental-request"),
    path("notifications/", NotificationView.as_view()),
    path("notifications/<int:id>/read/", MarkNotificationReadView.as_view()),
]
