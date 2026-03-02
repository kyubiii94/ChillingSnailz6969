from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ("email", "username", "is_staff", "gdpr_consent", "is_anonymized")
    list_filter = ("is_staff", "is_active", "gdpr_consent", "is_anonymized")
    search_fields = ("email", "username")
    ordering = ("email",)
    fieldsets = UserAdmin.fieldsets + (
        ("Web3", {"fields": ("wallet_address",)}),
        ("RGPD", {"fields": ("gdpr_consent", "gdpr_consent_date", "data_retention_until", "is_anonymized")}),
    )
