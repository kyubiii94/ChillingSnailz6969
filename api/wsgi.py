"""
Point d'entrée WSGI pour le déploiement Vercel.
Expose l'application Django sous le nom attendu par Vercel : app.
"""
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.vercel")

from django.core.wsgi import get_wsgi_application

app = get_wsgi_application()
