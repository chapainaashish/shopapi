import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_DEFAULT", os.getenv("DJANGO_SETTINGS_MODULE"))


celery = Celery("shopapi")

celery.config_from_object("django.conf:settings", namespace="CELERY")

celery.autodiscover_tasks()
