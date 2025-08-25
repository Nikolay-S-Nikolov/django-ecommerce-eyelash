from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from lash_store.accounts.models import Profile

User_model = get_user_model()

@receiver(post_save, sender=User_model)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)