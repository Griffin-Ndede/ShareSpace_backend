from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()
# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile", null=True)

    # contact info
    phone_number = models.CharField(max_length=20, blank=True)

    # profile info
    profile_photo = models.ImageField(upload_to="profile_pics/", blank=True, null=True)
    bio = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

    def __str__(self):
        return f"{self.user.username}'s Profile"
