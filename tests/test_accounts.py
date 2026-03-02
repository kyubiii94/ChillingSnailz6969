import pytest
from django.urls import reverse

from apps.accounts.models import CustomUser


@pytest.mark.django_db
class TestRegistration:
    def test_register_page_loads(self, anon_client):
        resp = anon_client.get(reverse("accounts:register"))
        assert resp.status_code == 200
        assert b"CREER MON COMPTE" in resp.content

    def test_register_creates_user(self, anon_client):
        resp = anon_client.post(reverse("accounts:register"), {
            "email": "new@example.com",
            "username": "newuser",
            "password1": "Str0ngP@ss!2024",
            "password2": "Str0ngP@ss!2024",
            "gdpr_consent": True,
        })
        assert resp.status_code == 302
        user = CustomUser.objects.get(email="new@example.com")
        assert user.gdpr_consent is True
        assert user.gdpr_consent_date is not None

    def test_register_without_gdpr_fails(self, anon_client):
        resp = anon_client.post(reverse("accounts:register"), {
            "email": "nogdpr@example.com",
            "username": "nogdpr",
            "password1": "Str0ngP@ss!2024",
            "password2": "Str0ngP@ss!2024",
        })
        assert resp.status_code == 200
        assert not CustomUser.objects.filter(email="nogdpr@example.com").exists()

    def test_register_weak_password_fails(self, anon_client):
        resp = anon_client.post(reverse("accounts:register"), {
            "email": "weak@example.com",
            "username": "weakuser",
            "password1": "123",
            "password2": "123",
            "gdpr_consent": True,
        })
        assert resp.status_code == 200
        assert not CustomUser.objects.filter(email="weak@example.com").exists()


@pytest.mark.django_db
class TestProfile:
    def test_profile_requires_auth(self, anon_client):
        resp = anon_client.get(reverse("accounts:profile"))
        assert resp.status_code == 302
        assert "/accounts/" in resp.url

    def test_profile_loads_for_authenticated(self, auth_client, user):
        resp = auth_client.get(reverse("accounts:profile"))
        assert resp.status_code == 200
        assert user.email.encode() in resp.content


@pytest.mark.django_db
class TestGDPRExport:
    def test_export_requires_auth(self, anon_client):
        resp = anon_client.get(reverse("accounts:export-data"))
        assert resp.status_code == 302

    def test_export_returns_json(self, auth_client, user):
        resp = auth_client.get(reverse("accounts:export-data"))
        assert resp.status_code == 200
        data = resp.json()
        assert data["personal_data"]["email"] == user.email
        assert "export_date" in data


@pytest.mark.django_db
class TestGDPRDelete:
    def test_delete_requires_post(self, auth_client):
        resp = auth_client.get(reverse("accounts:delete-account"))
        assert resp.status_code == 405

    def test_delete_anonymizes_user(self, auth_client, user):
        resp = auth_client.post(reverse("accounts:delete-account"))
        assert resp.status_code == 302
        user.refresh_from_db()
        assert user.is_anonymized is True
        assert user.is_active is False
        assert "anonymized" in user.email


@pytest.mark.django_db
class TestCustomUserManager:
    def test_create_user(self):
        user = CustomUser.objects.create_user(
            email="manager@test.com", password="TestP@ss!2024",
        )
        assert user.email == "manager@test.com"
        assert user.is_active is True
        assert user.is_staff is False

    def test_create_user_no_email_raises(self):
        with pytest.raises(ValueError, match="obligatoire"):
            CustomUser.objects.create_user(email="", password="Test")

    def test_create_superuser(self):
        admin = CustomUser.objects.create_superuser(
            email="super@test.com", password="TestP@ss!2024",
        )
        assert admin.is_staff is True
        assert admin.is_superuser is True
