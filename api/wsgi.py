"""
Point d'entrée WSGI pour le déploiement Vercel.
Expose l'application Django sous le nom attendu par Vercel : app.
"""
import os
import shutil
from pathlib import Path

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.vercel")

# Sur Vercel Lambda, seul /tmp est inscriptible.
# On copie la DB pré-migrée (générée au build) vers /tmp au premier démarrage.
_src = Path(__file__).resolve().parent.parent / "db.sqlite3"
_dst = Path("/tmp/db.sqlite3")
if _src.exists() and not _dst.exists():
    shutil.copy2(_src, _dst)

from django.core.wsgi import get_wsgi_application  # noqa: E402

app = get_wsgi_application()
