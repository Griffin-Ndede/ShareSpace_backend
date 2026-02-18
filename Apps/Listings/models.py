from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Listing(models.Model):
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="listings", null=True
    )

    # Step 1
    category = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    description = models.TextField()
    condition = models.CharField(max_length=255)
    accessories = models.CharField(max_length=255, blank=True, null=True)
    usage_rules = models.TextField(blank=True, null=True)

    # Step 2
    image_url = models.JSONField(default=list, blank=True)
    location = models.CharField(max_length=255)
    startDate = models.DateField(null=True, blank=True)
    endDate = models.DateField(null=True, blank=True)

    # Step 3
    dailyRate = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    weeklyRate = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    minPeriod = models.CharField(max_length=50, null=True, blank=True)
    deposit = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    depositRequirements = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.title
