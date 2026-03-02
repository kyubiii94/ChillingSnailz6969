from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    gdpr_consent = forms.BooleanField(
        required=True,
        label="J'accepte la politique de confidentialite et le traitement de mes donnees personnelles (RGPD).",
    )

    class Meta:
        model = CustomUser
        fields = ("email", "username", "password1", "password2", "gdpr_consent")

    def save(self, commit=True):
        user = super().save(commit=False)
        if self.cleaned_data.get("gdpr_consent"):
            from django.utils import timezone

            user.gdpr_consent = True
            user.gdpr_consent_date = timezone.now()
        if commit:
            user.save()
        return user
