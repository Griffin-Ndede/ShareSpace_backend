from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Listing(models.Model):
    STATUS_CHOICES = [
        ("pending_review", "Pending review"),
        ("changes_requested", "Changes requested"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    ]

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="listings",
        null=True,
    )

    # Step 1: Listing details
    category = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    description = models.TextField()
    condition = models.CharField(max_length=255)
    accessories = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )
    usage_rules = models.TextField(
        blank=True,
        null=True,
    )

    # Step 2: Images, location and availability
    image_url = models.JSONField(
        default=list,
        blank=True,
    )
    location = models.CharField(max_length=255)
    startDate = models.DateField(
        null=True,
        blank=True,
    )
    endDate = models.DateField(
        null=True,
        blank=True,
    )

    # Step 3: Pricing
    dailyRate = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
    )
    weeklyRate = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
    )
    minPeriod = models.CharField(
        max_length=50,
        null=True,
        blank=True,
    )
    deposit = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
    )
    depositRequirements = models.TextField(
        blank=True,
        null=True,
    )

    # Moderation
    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default="pending_review",
        db_index=True,
    )
    review_notes = models.TextField(
        blank=True,
        null=True,
    )
    reviewed_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="reviewed_listings",
    )
    reviewed_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    # Timestamps
    created_at = models.DateTimeField(
        auto_now_add=True,
        null=True,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        null=True,
    )

    def __str__(self):
        return self.title


class RentalRequest(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("accepted", "Accepted"),
        ("rejected", "Rejected"),
        ("completed", "Completed"),
    ]

    listing = models.ForeignKey(
        Listing,
        on_delete=models.CASCADE,
        related_name="rental_requests",
    )
    renter = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="rental_requests",
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="received_requests",
    )

    start_date = models.DateField()
    end_date = models.DateField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending",
        db_index=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
    )

    def __str__(self):
        return f"{self.renter.username} - " f"{self.listing.title} ({self.status})"


class Notification(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="notifications",
    )
    title = models.CharField(max_length=255)
    message = models.TextField()
    link = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.username} - {self.title}"


class ListingModerationEvent(models.Model):
    ACTION_CHOICES = [
        ("approved", "Approved"),
        ("changes_requested", "Changes requested"),
        ("rejected", "Rejected"),
        ("resubmitted", "Resubmitted"),
    ]

    listing = models.ForeignKey(
        Listing,
        on_delete=models.SET_NULL,
        null=True,
        related_name="moderation_events",
    )
    moderator = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="listing_moderation_events",
    )
    action = models.CharField(
        max_length=30,
        choices=ACTION_CHOICES,
        db_index=True,
    )
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.action} - listing {self.listing_id}"
