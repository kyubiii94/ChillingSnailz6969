import structlog

from .models import AuditLog

logger = structlog.get_logger(__name__)

AUDITED_PATHS = {
    "/accounts/login/": AuditLog.Action.LOGIN,
    "/accounts/logout/": AuditLog.Action.LOGOUT,
    "/accounts/register/": AuditLog.Action.REGISTER,
    "/accounts/profile/": AuditLog.Action.PROFILE_VIEW,
    "/accounts/export-data/": AuditLog.Action.DATA_EXPORT,
    "/accounts/delete-account/": AuditLog.Action.ACCOUNT_DELETE,
}


def _get_client_ip(request):
    x_forwarded = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded:
        return x_forwarded.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR")


class AuditMiddleware:
    """Log sensitive actions to the audit trail."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if request.method == "POST" and request.path in AUDITED_PATHS:
            action = AUDITED_PATHS[request.path]
            if response.status_code < 400:
                user = request.user if request.user.is_authenticated else None
                AuditLog.objects.create(
                    user=user,
                    action=action,
                    ip_address=_get_client_ip(request),
                    user_agent=request.META.get("HTTP_USER_AGENT", "")[:512],
                )
                logger.info("audit_event", action=action, user_id=getattr(user, "id", None))

        return response
