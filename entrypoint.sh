#!/bin/sh

# Check if DJANGO_SETTINGS_MODULE is set to 'shopapi.settings.production'
if [ "$DJANGO_SETTINGS_MODULE" = "shopapi.settings.production" ]; then
    echo 'Waiting for PostgreSQL...'
    while ! nc -z "$DB_HOST" "$DB_PORT"; do
        sleep 0.1
    done
    echo 'PostgreSQL started'
fi

echo 'Running migrations...'
python manage.py migrate

echo 'Collecting static files...'
python manage.py collectstatic --no-input

# for executing positional arguments
exec "$@"