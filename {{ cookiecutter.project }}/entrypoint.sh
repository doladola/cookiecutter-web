#!/usr/bin/env sh
set -eu

case "${1:-web-dev}" in
  web-dev)
    python manage.py migrate --noinput
    exec python manage.py runserver 0.0.0.0:8000
    ;;
  web-prod)
    python manage.py migrate --noinput
    python manage.py collectstatic --noinput
    exec gunicorn {{ cookiecutter.project }}.wsgi:application --bind 0.0.0.0:8000 --workers "${GUNICORN_WORKERS:-4}" --threads "${GUNICORN_THREADS:-4}"
    ;;
  celery-worker)
    exec celery -A {{ cookiecutter.project }} worker -l info
    ;;
  celery-beat)
    python manage.py migrate --noinput
    exec celery -A {{ cookiecutter.project }} beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler
    ;;
  *)
    exec "$@"
    ;;
esac
