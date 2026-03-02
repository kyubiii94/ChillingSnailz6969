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

# SQLite dans /tmp — seul répertoire inscriptible sur Vercel Lambda
# (le wsgi.py copie le fichier pré-migré depuis le projet au démarrage)
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "/tmp/db.sqlite3",
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

# Logging sans handler fichier : le filesystem est read-only sur Lambda,
# RotatingFileHandler ferait crasher la fonction au démarrage.
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "json": {
            "()": "structlog.stdlib.ProcessorFormatter",
            "processor": "structlog.dev.ConsoleRenderer",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "json",
        },
    },
    "root": {"handlers": ["console"], "level": "INFO"},
    "loggers": {
        "django": {"handlers": ["console"], "level": "INFO", "propagate": False},
        "django.security": {"handlers": ["console"], "level": "WARNING", "propagate": False},
        "apps": {"handlers": ["console"], "level": "INFO", "propagate": False},
    },
}
