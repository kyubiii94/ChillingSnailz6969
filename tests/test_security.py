import pytest
from django.test import Client, override_settings
from django.urls import reverse


@pytest.mark.django_db
class TestCSRFProtection:
    def test_post_without_csrf_rejected(self):
        client = Client(enforce_csrf_checks=True)
        resp = client.post(reverse("accounts:register"), {
            "email": "csrf@test.com",
            "username": "csrfuser",
            "password1": "TestP@ssword!2024",
            "password2": "TestP@ssword!2024",
            "gdpr_consent": True,
        })
        assert resp.status_code == 403


@pytest.mark.django_db
class TestXSSProtection:
    def test_template_escapes_html(self, auth_client, user):
        user.username = "<script>alert('xss')</script>"
        user.save()
        resp = auth_client.get(reverse("accounts:profile"))
        assert b"<script>" not in resp.content
        assert b"&lt;script&gt;" in resp.content


@pytest.mark.django_db
class TestAuthRequired:
    PROTECTED_URLS = [
        "accounts:profile",
        "accounts:export-data",
    ]

    @pytest.mark.parametrize("url_name", PROTECTED_URLS)
    def test_redirect_to_login(self, anon_client, url_name):
        resp = anon_client.get(reverse(url_name))
        assert resp.status_code == 302
        assert "/accounts/" in resp.url


@pytest.mark.django_db
class TestSecurityHeaders:
    @override_settings(
        SECURE_CONTENT_TYPE_NOSNIFF=True,
        X_FRAME_OPTIONS="DENY",
    )
    def test_x_frame_options(self, anon_client):
        resp = anon_client.get(reverse("core:home"))
        assert resp.get("X-Frame-Options") == "DENY"

    @override_settings(SECURE_CONTENT_TYPE_NOSNIFF=True)
    def test_content_type_nosniff(self, anon_client):
        resp = anon_client.get(reverse("core:home"))
        assert resp.get("X-Content-Type-Options") == "nosniff"


@pytest.mark.django_db
class TestPasswordSecurity:
    def test_argon2_is_default_hasher(self):
        from django.conf import settings
        assert "Argon2" in settings.PASSWORD_HASHERS[0]

    def test_min_password_length(self):
        from django.conf import settings
        validators = settings.AUTH_PASSWORD_VALIDATORS
        length_validator = next(
            v for v in validators
            if "MinimumLength" in v["NAME"]
        )
        assert length_validator["OPTIONS"]["min_length"] >= 10
