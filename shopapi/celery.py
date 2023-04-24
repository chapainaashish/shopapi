import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_DEFAULT", "storefront.settings")


celery = Celery("shopapi")

celery.config_from_object("django.conf:settings", namespace="CELERY")

celery.autodiscover_tasks()
