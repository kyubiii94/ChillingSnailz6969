# Checklist de Securite OWASP Top 10 — Chilling Snailz

## A01:2021 - Broken Access Control

- [x] RBAC via Django groups/permissions
- [x] `@login_required` sur les vues sensibles (profil, mint, export)
- [x] CSRF protection activee (middleware + `{% csrf_token %}`)
- [x] `X-Frame-Options: DENY`
- [x] Permissions DRF par defaut: `IsAuthenticated`

## A02:2021 - Cryptographic Failures

- [x] Mots de passe haches avec Argon2 (`PASSWORD_HASHERS`)
- [x] TLS/HTTPS obligatoire (`SECURE_SSL_REDIRECT`)
- [x] HSTS active (31 536 000s)
- [x] Champs sensibles chiffrables (wallet, tx_hash)
- [x] Secrets dans `.env`, jamais en dur

## A03:2021 - Injection

- [x] ORM Django (requetes parametrees, pas de `raw()`)
- [x] Validation des entrees via Django Forms et DRF serializers
- [x] Echappement auto des templates Django (XSS)

## A04:2021 - Insecure Design

- [x] Architecture MVC/MVT propre
- [x] Separation des settings (dev/prod)
- [x] Principe du moindre privilege (user DB dedie)

## A05:2021 - Security Misconfiguration

- [x] `DEBUG = False` en production
- [x] Headers de securite (CSP, X-Content-Type-Options, Referrer-Policy)
- [x] Docker avec user non-root
- [x] Image minimale (python:3.12-slim)

## A06:2021 - Vulnerable and Outdated Components

- [x] `safety check` dans CI
- [x] `bandit` analyse statique dans CI
- [x] Dependances avec contraintes de version

## A07:2021 - Identification and Authentication Failures

- [x] Rate limiting login (django-axes, 5 tentatives)
- [x] Session timeout 1h
- [x] Verification email obligatoire (allauth)
- [x] Password validators (longueur min 10, pas commun, pas similaire)

## A08:2021 - Software and Data Integrity Failures

- [x] CI/CD avec tests automatises
- [x] Docker build dans CI
- [x] Pas de deserialization non securisee

## A09:2021 - Security Logging and Monitoring Failures

- [x] Audit trail (AuditLog model)
- [x] Logging structure (structlog)
- [x] Sentry pour tracking d'erreurs
- [x] Pas de PII dans les logs

## A10:2021 - Server-Side Request Forgery (SSRF)

- [x] Pas d'appels HTTP cote serveur base sur input utilisateur
- [x] Nginx comme reverse proxy (pas d'acces direct)
