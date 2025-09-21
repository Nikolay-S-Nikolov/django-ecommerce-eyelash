from django.db import models

class ContactInfo(models.Model):
    MAX_PHONE_NUMBER_LENGTH = 14

    phone_number = models.CharField(
        max_length=MAX_PHONE_NUMBER_LENGTH,
        verbose_name="Телефонен номер",
        help_text="Въведи телефонен номер във формат +359..."
    )
    working_time = models.TextField()
    address = models.TextField(max_length=200)
    custom_message = models.TextField()
    visible = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Контактна информация"
        verbose_name_plural = "Контактни данни"
        ordering = ['-created_at']

    def __str__(self):
        return f"Информация за контакти тел:{self.phone_number} създадена на {self.created_at}"

class SocialLink(models.Model):
    ICON_CHOICES = [
        ('fa-facebook', 'Facebook'),
        ('fa-instagram', 'Instagram'),
        ('fa-twitter', 'Twitter'),
        ('fa-youtube', 'YouTube'),
        ('fa-linkedin', 'LinkedIn'),
        ('fa-globe', 'Уебсайт'),
        ('fa-link', 'Общ линк'),
        ('custom', 'Ръчно въвеждане'),
    ]

    label = models.CharField(max_length=50)
    url = models.URLField()
    icon_class = models.CharField(
        max_length=50,
        choices=ICON_CHOICES,
        default='custom',
        help_text="Избери икона за социалната платформа или избери 'Ръчно' за персонализирана стойност"
    )

    custom_icon = models.CharField(
        max_length=50,
        blank=True,
        help_text="Ако е избрано 'Ръчно', въведи CSS клас за иконата (напр. 'fa-tiktok')"
    )
    appearance_order = models.PositiveIntegerField(
        default=1,
    )

    def get_icon(self):
        return self.custom_icon if self.icon_class == 'custom' else self.icon_class

    def __str__(self):
        return f"{self.label} ({self.get_icon()})"
