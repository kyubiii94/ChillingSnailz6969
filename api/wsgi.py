"""
Point d'entrée WSGI pour le déploiement Vercel.
Expose l'application Django sous le nom attendu par Vercel : app.
"""
import os
import shutil
from pathlib import Path

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.vercel")

_src = Path(__file__).resolve().parent.parent / "db.sqlite3"
_dst = Path("/tmp/db.sqlite3")

# Cas 1 : DB pré-migrée présente dans le bundle → on la copie dans /tmp (writable).
if _src.exists() and not _dst.exists():
    shutil.copy2(_src, _dst)

# Cas 2 : DB absente (gitignored, non incluse par Vercel) → migration à la volée.
# C'est un coût au cold-start (~1 s) mais garanti correct.
if not _dst.exists():
    import django  # noqa: E402
    django.setup()
    from django.core.management import call_command  # noqa: E402
    call_command("migrate", "--noinput", verbosity=0)

from django.core.wsgi import get_wsgi_application  # noqa: E402

app = get_wsgi_application()
