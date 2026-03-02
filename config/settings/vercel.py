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

# Cache en mémoire — LocMemCache supporte l'incrément atomique requis par
# django-ratelimit. DatabaseCache ne le supporte pas, et Redis n'est pas
# disponible par défaut sur Vercel serverless.
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
    }
}

# WhiteNoise pour servir les fichiers statiques en production
MIDDLEWARE.insert(1, "whitenoise.middleware.WhiteNoiseMiddleware")  # noqa: F405
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Désactiver des options lourdes non nécessaires en serverless
AXES_ENABLED = False
ACCOUNT_EMAIL_VERIFICATION = "optional"

# Sur Vercel serverless il n'y a pas de cache partagé entre instances.
# LocMemCache supporte l'incrément atomique et fonctionne par process.
# On silence les checks qui exigent un backend partagé (Redis/Memcached).
SILENCED_SYSTEM_CHECKS = [
    "django_ratelimit.E003",
    "django_ratelimit.W001",
]
