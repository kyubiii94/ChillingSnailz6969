"""
GDPR compliance utilities:
- Right to be forgotten (anonymization)
- Data portability (export)
- Retention cleanup
"""
import hashlib
import uuid

from django.utils import timezone

from .models import AuditLog


def anonymize_user(user):
    """
    Anonymize a user account (GDPR right to be forgotten).
    Replaces PII with hashed/random values, keeps anonymized records
    for audit integrity.
    """
    anonymous_hash = hashlib.sha256(str(uuid.uuid4()).encode()).hexdigest()[:16]
    user.email = f"deleted_{anonymous_hash}@anonymized.local"
    user.username = f"deleted_{anonymous_hash}"
    user.wallet_address = ""
    user.first_name = ""
    user.last_name = ""
    user.is_active = False
    user.is_anonymized = True
    user.set_unusable_password()
    user.save()

    AuditLog.objects.create(
        user=user,
        action=AuditLog.Action.ACCOUNT_DELETE,
        details={"method": "gdpr_anonymization"},
    )


def export_user_data(user):
    """
    Export all personal data for a user (GDPR data portability).
    Returns a dict suitable for JSON serialization.
    """
    from apps.nft.models import MintTransaction, Snailz

    snailz_owned = Snailz.objects.filter(owner=user).values(
        "token_id", "rarity", "is_major", "faction__name",
    )
    transactions = MintTransaction.objects.filter(user=user).values(
        "tx_hash", "amount_eth", "status", "created_at",
    )

    return {
        "personal_data": {
            "email": user.email,
            "username": user.username,
            "wallet_address": user.wallet_address,
            "date_joined": user.date_joined.isoformat(),
            "gdpr_consent": user.gdpr_consent,
            "gdpr_consent_date": user.gdpr_consent_date.isoformat() if user.gdpr_consent_date else None,
        },
        "nfts_owned": list(snailz_owned),
        "mint_transactions": [
            {**t, "amount_eth": str(t["amount_eth"]), "created_at": t["created_at"].isoformat()}
            for t in transactions
        ],
        "export_date": timezone.now().isoformat(),
    }


def cleanup_inactive_accounts(retention_days=730):
    """
    Anonymize accounts that have exceeded their data retention period.
    Called by the Celery beat schedule.
    """
    from apps.accounts.models import CustomUser

    cutoff = timezone.now() - timezone.timedelta(days=retention_days)
    expired_users = CustomUser.objects.filter(
        is_anonymized=False,
        last_login__lt=cutoff,
        data_retention_until__lt=timezone.now(),
    ).exclude(is_staff=True)

    count = 0
    for user in expired_users:
        anonymize_user(user)
        count += 1
    return count
