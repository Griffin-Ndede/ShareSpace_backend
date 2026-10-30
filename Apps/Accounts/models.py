
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = models.EmailField(unique=True)

    ROLE_CHOICES = [
        ("rentee", "Rentee"),
        ("renter", "Renter"),
        ("both", "Both"),
    ]

    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default="rentee",
        db_index=True,
    )
    VERIFICATION_CHOICES = [
        ("unverified", "Unverified"),
        ("pending", "Pending verification"),
        ("verified", "Verified"),
        ("rejected", "Verification rejected"),
    ]
    verification_status = models.CharField(
        max_length=20,
        choices=VERIFICATION_CHOICES,
        default="unverified",
        db_index=True,
    )

    verification_notes = models.TextField(
        blank=True,
        null=True,
    )

    verified_by = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="verified_users",
    )

    verified_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.get_full_name() or self.username
