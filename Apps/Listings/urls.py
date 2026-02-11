from django.urls import path
from .views import ListingView, ListingDetailView, myListingsView

urlpatterns = [
    path("listing/", ListingView.as_view(), name="listing"),
    path("listing/<int:id>/", ListingDetailView.as_view(), name="listing-detail"),
    path("my-listings/", myListingsView.as_view(), name="my-listings"),
    path("my-listings/<int:id>/", myListingsView.as_view(), name="my-listing-delete"),
]
