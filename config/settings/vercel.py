"""
Settings pour le déploiement sur Vercel (serverless).
- SQLite (pas de PostgreSQL en serverless)
- WhiteNoise pour servir les fichiers statiques
- ALLOWED_HOSTS inclut *.vercel.app
"""
import os

# Définir SECRET_KEY et ALLOWED_HOSTS avant d'importer base (pas de .env sur Vercel)
if "SECRET_KEY" not in os.environ:
    os.environ.setdefault("SECRET_KEY", "vercel-secret-key-change-in-dashboard")
if "ALLOWED_HOSTS" not in os.environ:
    os.environ.setdefault("ALLOWED_HOSTS", ".vercel.app,.now.sh,localhost,127.0.0.1")

from .base import *  # noqa: F401, F403

DEBUG = False
ALLOWED_HOSTS = [
    ".vercel.app",
    ".now.sh",
    "localhost",
    "127.0.0.1",
    "chilling-snailz6969.vercel.app",
]

# SQLite pour Vercel (pas de DB externe par défaut)
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",  # noqa: F405
    }
}

# Cache partagé (requis par django_ratelimit) — database cache avec SQLite
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.db.DatabaseCache",
        "LOCATION": "vercel_cache_table",
    }
}

# WhiteNoise pour servir les fichiers statiques en production
MIDDLEWARE.insert(1, "whitenoise.middleware.WhiteNoiseMiddleware")  # noqa: F405
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Désactiver des options lourdes non nécessaires en serverless
AXES_ENABLED = False
ACCOUNT_EMAIL_VERIFICATION = "optional"
