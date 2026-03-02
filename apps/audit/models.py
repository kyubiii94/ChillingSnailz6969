from django.conf import settings
from django.db import models


class AuditLog(models.Model):
    """Immutable audit trail for sensitive operations. No PII stored in details."""

    class Action(models.TextChoices):
        LOGIN = "login", "Login"
        LOGOUT = "logout", "Logout"
        LOGIN_FAILED = "login_failed", "Login Failed"
        REGISTER = "register", "Register"
        PROFILE_VIEW = "profile_view", "Profile View"
        DATA_EXPORT = "data_export", "Data Export"
        ACCOUNT_DELETE = "account_delete", "Account Delete"
        MINT = "mint", "Mint"
        PASSWORD_CHANGE = "password_change", "Password Change"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name="audit_logs",
    )
    action = models.CharField(max_length=100, choices=Action.choices)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.CharField(max_length=512, blank=True, default="")
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)
    details = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ["-timestamp"]
        indexes = [
            models.Index(fields=["user", "action"]),
        ]

    def __str__(self):
        user_str = f"user={self.user_id}" if self.user_id else "anonymous"
        return f"[{self.timestamp:%Y-%m-%d %H:%M}] {self.action} — {user_str}"
