import pytest
from django.urls import reverse

from apps.audit.gdpr import anonymize_user, export_user_data
from apps.audit.models import AuditLog


@pytest.mark.django_db
class TestAuditLog:
    def test_create_audit_entry(self, user):
        log = AuditLog.objects.create(
            user=user, action=AuditLog.Action.LOGIN,
            ip_address="127.0.0.1",
        )
        assert log.action == "login"
        assert "login" in str(log)

    def test_audit_middleware_on_register(self, anon_client):
        anon_client.post(reverse("accounts:register"), {
            "email": "audit@example.com",
            "username": "audituser",
            "password1": "Str0ngP@ss!2024",
            "password2": "Str0ngP@ss!2024",
            "gdpr_consent": True,
        })
        assert AuditLog.objects.filter(action="register").exists()


@pytest.mark.django_db
class TestGDPRAnonymization:
    def test_anonymize_user(self, user):
        original_email = user.email
        anonymize_user(user)
        user.refresh_from_db()
        assert user.is_anonymized is True
        assert user.is_active is False
        assert original_email not in user.email
        assert "anonymized" in user.email
        assert user.wallet_address == ""
        assert not user.has_usable_password()

    def test_anonymize_creates_audit_log(self, user):
        anonymize_user(user)
        assert AuditLog.objects.filter(
            user=user, action="account_delete",
        ).exists()


@pytest.mark.django_db
class TestGDPRExport:
    def test_export_contains_personal_data(self, user):
        data = export_user_data(user)
        assert data["personal_data"]["email"] == user.email
        assert "nfts_owned" in data
        assert "mint_transactions" in data
        assert "export_date" in data
