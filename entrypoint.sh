#!/bin/sh

echo 'Waiting for postgress'

while ! nc -z $NAME $PORT; do
    sleep 0.1
done


echo 'PostgreSQL finally started'

echo 'Running migrations...'

python manage.py migrate

echo 'Collecting static files...'

python manage.py collectstatic --no-input


# for executing positional arguments
exec "$@"