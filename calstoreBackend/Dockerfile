# ──────────────────────────────────────────────
# Image de base : Python slim pour garder l'image légère
# ──────────────────────────────────────────────
FROM python:3.11-slim

# Empêche la génération de .pyc et force les logs en temps réel
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# ──────────────────────────────────────────────
# Dépendances système
# ──────────────────────────────────────────────
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    libjpeg-dev \
    zlib1g-dev \
    # Nécessaire pour attendre que Postgres soit prêt dans entrypoint.sh
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

# ──────────────────────────────────────────────
# Dépendances Python (en premier pour profiter du cache Docker)
# ──────────────────────────────────────────────
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ──────────────────────────────────────────────
# Code source
# ──────────────────────────────────────────────
COPY . .

# ──────────────────────────────────────────────
# Script d'entrée : migrations + démarrage Gunicorn
# ──────────────────────────────────────────────
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["/entrypoint.sh"]

# Gunicorn en production (remplace runserver)
# calstoreBackend.wsgi = chemin vers ton fichier wsgi.py
CMD ["gunicorn", "calstoreBackend.wsgi:application", \
     "--bind", "0.0.0.0:8000", \
     "--workers", "3", \
     "--timeout", "120", \
     "--access-logfile", "-"]