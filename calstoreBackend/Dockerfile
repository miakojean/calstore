# Utilisation d'une image Python légère
FROM python:3.11-slim

# Empêche Python de générer des fichiers .pyc et assure l'affichage direct des logs
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Installation des dépendances système nécessaires (Postgres, Pillow, etc.)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    libjpeg-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# Installation des dépendances Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie du projet
COPY . .

# Script de lancement (optionnel, utile pour les migrations)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]