from django.urls import path
from .views import ListingView, ListingDetailView

urlpatterns = [
    path("listing/", ListingView.as_view(), name="listing"),
    path("listing/<int:id>/", ListingDetailView.as_view(), name="listing-detail")
]