###############################################################################
# Stage 1: Build dependencies
###############################################################################
FROM python:3.12-slim AS builder

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc libpq-dev && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

###############################################################################
# Stage 2: Production image (minimal)
###############################################################################
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update && \
    apt-get install -y --no-install-recommends libpq5 && \
    rm -rf /var/lib/apt/lists/* && \
    addgroup --system django && \
    adduser --system --ingroup django django

WORKDIR /app

COPY --from=builder /install /usr/local
COPY . .

RUN python manage.py collectstatic --noinput --settings=config.settings.production 2>/dev/null || true && \
    mkdir -p /app/logs /app/media && \
    chown -R django:django /app

USER django

EXPOSE 8000

CMD ["gunicorn", "config.wsgi:application", \
     "--bind", "0.0.0.0:8000", \
     "--workers", "3", \
     "--timeout", "120", \
     "--access-logfile", "-", \
     "--error-logfile", "-"]
