#!/bin/sh
# ──────────────────────────────────────────────
# entrypoint.sh — attend Postgres, puis migre et démarre
# ──────────────────────────────────────────────

set -e

echo "⏳ En attente de la base de données..."

# Attend que Postgres accepte les connexions (max 30 tentatives)
until nc -z "$DB_HOST" 5432; do
  sleep 1
done

echo "✅ Base de données disponible."

echo "🔄 Application des migrations..."
python manage.py migrate --noinput

echo "📦 Collecte des fichiers statiques..."
python manage.py collectstatic --noinput

echo "🚀 Démarrage du serveur..."
exec "$@"