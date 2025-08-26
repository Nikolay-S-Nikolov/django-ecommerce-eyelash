from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from allauth.account.signals import user_logged_in
from allauth.socialaccount.models import SocialAccount
from allauth.socialaccount.signals import social_account_added, social_account_updated

from lash_store.accounts.models import Profile

User_model = get_user_model()


@receiver(post_save, sender=User_model)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


def _update_profile_from_google(user):
    """
    Pull name and avatar from the user's Google SocialAccount and store them
    into Profile.preferred_name_nickname and Profile.profile_picture.
    - Do not overwrite a non-default preferred_name_nickname if the user has already set it.
    - Only set profile_picture if it's currently empty.
    """
    try:
        sa = SocialAccount.objects.get(user=user, provider='google')
    except SocialAccount.DoesNotExist:
        return

    extra = sa.extra_data or {}
    # Google typically returns: name, given_name, family_name, picture, email, sub, etc.
    name = extra.get('name') or extra.get('given_name')
    picture = extra.get('picture')

    profile, _ = Profile.objects.get_or_create(user=user)

    # Update nickname only if empty or default placeholder
    if name and (not profile.preferred_name_nickname or profile.preferred_name_nickname == 'Anonymous'):
        profile.preferred_name_nickname = name

    # Only set picture if empty; you may choose to always refresh if desired
    if picture and not profile.profile_picture:
        profile.profile_picture = picture

    profile.save(update_fields=['preferred_name_nickname', 'profile_picture'])


@receiver(social_account_added)
def handle_social_account_added(sender, request, sociallogin, **kwargs):
    """Triggered when a social account (e.g., Google) is first connected."""
    if sociallogin.account.provider == 'google':
        _update_profile_from_google(sociallogin.user)


@receiver(social_account_updated)
def handle_social_account_updated(sender, request, sociallogin, **kwargs):
    """Triggered when a social account gets updated/refreshed."""
    if sociallogin.account.provider == 'google':
        _update_profile_from_google(sociallogin.user)


@receiver(user_logged_in)
def handle_user_logged_in(sender, request, user, **kwargs):
    """
    Also ensure data is present on login. This helps cover cases where the
    Profile was created before connecting Google.
    """
    _update_profile_from_google(user)