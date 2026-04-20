import os

from celery import Celery


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "{{ cookiecutter.project }}.settings")

app = Celery("{{ cookiecutter.project }}")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
