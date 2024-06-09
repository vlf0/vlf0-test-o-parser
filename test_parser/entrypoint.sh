#!/bin/sh
which xvfb-run
python3 manage.py check_database && \
python3 manage.py makemigrations
python3 manage.py migrate
export DJANGO_SUPERUSER_USERNAME=admin
export DJANGO_SUPERUSER_EMAIL=admin@example.com
export DJANGO_SUPERUSER_PASSWORD=root
python3 manage.py createsuperuser --noinput
celery -A test_parser worker --loglevel=info &
python3 manage.py runserver 0.0.0.0:8000