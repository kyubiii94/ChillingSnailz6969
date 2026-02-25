# Guide de deploiement — Chilling Snailz

## Pre-requis

- Docker & Docker Compose
- Un domaine avec certificats SSL (Let's Encrypt)
- Serveur Linux (Ubuntu 22.04+)

## Etapes

### 1. Cloner le repo

```bash
git clone https://github.com/kyubiii94/ChillingSnailz6969.git
cd ChillingSnailz6969
```

### 2. Configurer l'environnement

```bash
cp .env.example .env
# Editer .env avec vos valeurs de production :
# - SECRET_KEY : generer avec `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`
# - DATABASE_URL : votre PostgreSQL
# - FIELD_ENCRYPTION_KEY : generer avec `python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"`
# - SENTRY_DSN : votre DSN Sentry
```

### 3. Certificats SSL

Placer vos certificats dans `nginx/ssl/` :
- `cert.pem`
- `key.pem`

Ou configurer Let's Encrypt via certbot.

### 4. Lancer

```bash
docker compose up -d --build
```

### 5. Creer le superuser

```bash
docker compose exec web python manage.py createsuperuser
```

### 6. Verifier

- https://votre-domaine.com — Site public
- https://votre-domaine.com/admin/ — Administration

## Maintenance

### Backups

```bash
docker compose exec web python scripts/backup_db.py
```

### Migrations

```bash
docker compose exec web python manage.py migrate
```

### Logs

```bash
docker compose logs -f web
docker compose logs -f celery
```

## Securite

- [ ] Changer le SECRET_KEY
- [ ] Configurer ALLOWED_HOSTS
- [ ] Activer les certificats SSL
- [ ] Configurer Sentry
- [ ] Lancer un scan OWASP ZAP
- [ ] Verifier les headers avec securityheaders.com
