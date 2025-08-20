from django.contrib.auth import models as auth_models
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.core.mail import send_mail

from lash_store.accounts.managers import LashUserManager


class LashUser(auth_models.AbstractBaseUser, auth_models.PermissionsMixin):
    MAX_USER_NAME_LENGTH = 300

    email = models.EmailField(
        _("email address"),
        unique=True,
        help_text=_(
            "Required. Please enter your email address"
        ),
        error_messages={
            "unique": _("A user with this email already exists."),
        },
    )

    user_name = models.CharField(
        _("full name"),
        max_length=MAX_USER_NAME_LENGTH,
        help_text=_(
            "You can enter your name for personalized communication"
        ),
        blank=True,
        null=True,
    )

    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )

    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )

    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    objects = LashUserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def __str__(self):
        return self.email


class Profile(models.Model):
    MAX_PHONE_LENGTH = 10
    MAX_PREFERRED_NAME_NICKNAME_LENGTH = 150

    user = models.OneToOneField(
        LashUser,
        on_delete=models.CASCADE,
        primary_key=True,
    )

    preferred_name_nickname = models.CharField(
        max_length=MAX_PREFERRED_NAME_NICKNAME_LENGTH,
        help_text=_(
            "Please enter preferred name/nickname for personalized communication"
        ),
        default="Anonymous",
        blank=True,
    )

    phone_number = models.CharField(
        max_length=MAX_PHONE_LENGTH,
        null=True,
        blank=True,
        validators=[RegexValidator(
            regex=r"^0\d{9}$",
            message="Please, enter a valid phone number in the format 0888123456"
        )]
    )

    profile_picture = models.URLField(blank=True, null=True)

    def get_profile_name(self):
        """
        Return the name if any or Anonymous user.
        """
        if self.preferred_name_nickname:
            return self.preferred_name_nickname

        if self.user.user_name:
            return self.user.user_name

        return "Anonymous"

    def __str__(self):
        return self.user
