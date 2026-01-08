#!/bin/bash
set -e

echo "🚀 Démarrage de webappden..."

# Attendre que la base de données soit prête
echo "⏳ Attente de la base de données..."
while ! nc -z ${DB_HOST} ${DB_PORT}; do
  sleep 1
done
echo "✅ Base de données prête!"

# Exécuter les migrations
echo "📦 Exécution des migrations..."
python manage.py migrate --noinput

# Collecter les fichiers statiques
echo "🎨 Collecte des fichiers statiques..."
python manage.py collectstatic --noinput

echo "✨ Démarrage de Gunicorn..."
exec gunicorn --bind 0.0.0.0:8000 --workers 3 webappden.wsgi:application
