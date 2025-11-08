#!/usr/bin/env bash
set -e

# Exportar variables desde .env si existe
if [ -f /app/.env ]; then
  set -a
  . /app/.env
  set +a
fi

# (Opcional) validar que settings.ini exista y advertir si falta
if [ ! -f /app/settings.ini ]; then
  echo "WARNING: settings.ini no encontrado en /app/settings.ini"
fi

# Migraciones
python manage.py makemigrations --noinput || true
python manage.py migrate --noinput

# Iniciar server (reemplaza por gunicorn si quieres producción)
exec python manage.py runserver 0.0.0.0:8020
