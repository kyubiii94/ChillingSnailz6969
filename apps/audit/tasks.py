import structlog
from celery import shared_task

from .gdpr import cleanup_inactive_accounts

logger = structlog.get_logger(__name__)


@shared_task
def cleanup_inactive_accounts_task():
    """Periodic task: anonymize expired accounts per GDPR retention policy."""
    count = cleanup_inactive_accounts()
    logger.info("gdpr_cleanup_completed", anonymized_count=count)
    return count
