# admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import LashUser

@admin.register(LashUser)
class LashUserAdmin(UserAdmin):
    # Полетата са съобразени с email като USERNAME_FIELD
    ordering = ("email",)
    list_display = ("email", "user_name", "is_staff", "is_superuser", "is_active", "date_joined")
    search_fields = ("email", "user_name")

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal info"), {"fields": ("user_name",)}),
        (_("Permissions"), {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "password1", "password2", "is_staff", "is_superuser", "is_active"),
        }),
    )

    # Тъй като нямате username поле, указваме кои са основните идентификатори
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if "username" in form.base_fields:
            form.base_fields.pop("username")
        return form
