#!/usr/bin/env bash
set -euo pipefail

echo "[entrypoint] Starting entrypoint script..."

echo "[entrypoint] Running database migrations..."
python manage.py migrate --noinput

echo "[entrypoint] Collecting static files..."
python manage.py collectstatic --noinput

# 创建或更新管理员账号
echo "[entrypoint] Ensuring superuser exists..."
python manage.py shell <<'PYCODE'
from django.contrib.auth import get_user_model
User = get_user_model()
import os
username = os.environ.get("DJANGO_SUPERUSER_USERNAME", "admin")
email = os.environ.get("DJANGO_SUPERUSER_EMAIL", "{{ cookiecutter.project }}@{{ cookiecutter.project }}.com")
password = os.environ.get("DJANGO_SUPERUSER_PASSWORD", "admin12345")
created = False
if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    created = True
else:
    u = User.objects.get(username=username)
    changed = False
    if u.email != email:
        u.email = email
        changed = True
    if not u.has_usable_password():
        u.set_password(password)
        changed = True
    if changed:
        u.save()
print(f"[entrypoint] Superuser {'created' if created else 'ready'}: {username}")
PYCODE

echo "[entrypoint] Starting gunicorn..."
workers=${GUNICORN_WORKERS:-4}
threads=${GUNICORN_THREADS:-4}
exec gunicorn {{ cookiecutter.project }}.wsgi -w "$workers" -k gthread --threads "$threads" --bind 0.0.0.0:8000
