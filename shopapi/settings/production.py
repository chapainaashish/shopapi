import os

import sentry_sdk
from dotenv import load_dotenv

from .base import *

load_dotenv()

DEBUG = False
ALLOWED_HOSTS = ["*"]


sentry_sdk.init(
    dsn=os.getenv("SENTRY_DSN"),
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
)


INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # third party
    "corsheaders",
    "rest_framework",
    "djoser",
    "django_filters",
    "drf_spectacular",
    # local
    "user",
    "product",
    "order",
    "payment",
    "cart",
]


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": os.getenv("DB_NAME"),
        "USER": os.getenv("DB_USER"),
        "PASSWORD": os.getenv("DB_PASSWORD"),
        "HOST": os.getenv("DB_HOST"),
        "PORT": os.getenv("DB_PORT"),
    }
}


STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "file": {
            "class": "logging.FileHandler",
            "filename": "shopapi.log",
            "formatter": "verbose",
        },
    },
    "loggers": {
        "": {
            "handlers": ["file"],
            "level": os.getenv("DJANGO_LOG_LEVEL", "INFO"),
        }
    },
    "formatters": {
        "verbose": {
            "format": "{asctime} ({levelname})  - {name} - {message}",
            "style": "{",
        },
    },
}
