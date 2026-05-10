# syntax=docker/dockerfile:1.7
# =====================================================================
# Lash Store — Production image (multi-stage, non-root)
# =====================================================================

# ---------- Stage 1: build wheels ----------
FROM python:3.12-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        libpq-dev \
        libjpeg-dev \
        zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /build

COPY requirements.txt .
RUN pip wheel --wheel-dir /wheels -r requirements.txt

# ---------- Stage 2: runtime ----------
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    DJANGO_SETTINGS_MODULE=lash_store.settings \
    PORT=8000

# Runtime libs only (no compilers)
RUN apt-get update && apt-get install -y --no-install-recommends \
        libpq5 \
        libjpeg62-turbo \
        zlib1g \
    && rm -rf /var/lib/apt/lists/*

# Non-root user
RUN groupadd --system app && useradd --system --gid app --create-home app

WORKDIR /app

COPY --from=builder /wheels /wheels
RUN pip install --no-cache-dir /wheels/*.whl && rm -rf /wheels

# App source
COPY --chown=app:app . .

# Collect static files at build time. Dummy values are needed only because
# settings.py reads GOOGLE_CLIENT_ID / GOOGLE_CLIENT_SECRET eagerly.
RUN SECRET_KEY=build-only \
    GOOGLE_CLIENT_ID=build-only \
    GOOGLE_CLIENT_SECRET=build-only \
    DB_NAME=build DB_USER=build DB_PASSWORD=build DB_HOST=localhost DB_PORT=5432 \
    python manage.py collectstatic --noinput

USER app

EXPOSE 8000

# Run migrations then start gunicorn. For zero-downtime deployments, prefer
# running migrations as a separate release step on your platform.
CMD ["sh", "-c", "python manage.py migrate --noinput && gunicorn lash_store.wsgi:application --bind 0.0.0.0:${PORT} --workers 3 --timeout 60 --access-logfile - --error-logfile -"]
