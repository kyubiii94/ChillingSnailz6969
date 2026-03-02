from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

from .managers import CustomUserManager


class CustomUser(AbstractUser):
    """Extended user model with wallet and GDPR fields."""

    email = models.EmailField(unique=True)
    wallet_address = models.CharField(max_length=255, blank=True, default="")
    gdpr_consent = models.BooleanField(default=False)
    gdpr_consent_date = models.DateTimeField(null=True, blank=True)
    data_retention_until = models.DateTimeField(null=True, blank=True)
    is_anonymized = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = CustomUserManager()

    class Meta:
        verbose_name = "utilisateur"
        verbose_name_plural = "utilisateurs"

    def __str__(self):
        return self.email

    def give_consent(self):
        self.gdpr_consent = True
        self.gdpr_consent_date = timezone.now()
        self.save(update_fields=["gdpr_consent", "gdpr_consent_date"])

    def set_retention(self, years=2):
        self.data_retention_until = timezone.now() + timezone.timedelta(days=365 * years)
        self.save(update_fields=["data_retention_until"])
