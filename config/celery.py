"""Celery configuration for Chilling Snailz."""
import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.production")

app = Celery("chillingsnailz")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

app.conf.beat_schedule = {
    "gdpr-cleanup-inactive-accounts": {
        "task": "apps.audit.tasks.cleanup_inactive_accounts_task",
        "schedule": crontab(hour=3, minute=0),  # daily at 3 AM
    },
}
