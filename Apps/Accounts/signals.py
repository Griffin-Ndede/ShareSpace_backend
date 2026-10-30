from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

from Apps.Profile.models import UserProfile

User = get_user_model()


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        # Every newly registered user starts as a rentee.
        if instance.role != "rentee":
            instance.role = "rentee"
            instance.save(update_fields=["role"])

        # Create the user's profile if one does not already exist.
        UserProfile.objects.get_or_create(user=instance)