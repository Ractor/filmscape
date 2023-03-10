import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "filmscape.settings")

app = Celery("filmscape")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
