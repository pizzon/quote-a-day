#!/bin/sh

until cd /src/backend
do
    echo "Waiting for server volume..."
done




cd ..
# python manage.py createsuperuser --noinput

gunicorn quotes.wsgi --bind 0.0.0.0:8000 --workers 4 --threads 4

# for debug
#python manage.py runserver 0.0.0.0:8000