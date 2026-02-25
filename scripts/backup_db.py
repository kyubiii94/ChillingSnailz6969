#!/usr/bin/env python
"""
Automated PostgreSQL backup script with GPG encryption.
Run via cron or Celery beat:
    python scripts/backup_db.py
"""
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path


def backup():
    db_url = os.environ.get("DATABASE_URL", "")
    if not db_url:
        print("ERROR: DATABASE_URL not set")
        sys.exit(1)

    backup_dir = Path("/app/backups")
    backup_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = backup_dir / f"snailz_db_{timestamp}.sql.gz.gpg"

    dump_cmd = (
        f"pg_dump '{db_url}' "
        f"| gzip "
        f"| gpg --symmetric --batch --yes --passphrase-fd 0"
    )

    gpg_passphrase = os.environ.get("BACKUP_GPG_PASSPHRASE", "")
    if not gpg_passphrase:
        print("ERROR: BACKUP_GPG_PASSPHRASE not set")
        sys.exit(1)

    with open(filename, "wb") as f:
        proc = subprocess.Popen(
            dump_cmd, shell=True, stdin=subprocess.PIPE, stdout=f, stderr=subprocess.PIPE,
        )
        _, stderr = proc.communicate(input=gpg_passphrase.encode())

    if proc.returncode != 0:
        print(f"ERROR: Backup failed: {stderr.decode()}")
        sys.exit(1)

    print(f"OK: Backup created at {filename}")

    old_backups = sorted(backup_dir.glob("snailz_db_*.sql.gz.gpg"))[:-7]
    for old in old_backups:
        old.unlink()
        print(f"CLEANED: {old}")


if __name__ == "__main__":
    backup()
