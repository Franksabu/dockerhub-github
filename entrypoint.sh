#!/bin/sh

# Correct path to manage.py
python manage.py migrate --no-input
python manage.py collectstatic --no-input

# export PYTHONPATH=/app
# export DJANGO_SETTINGS_MODULE=docker_project.docker_project.settings
# echo "PYTHONPATH is set to: $PYTHONPATH"

# Correct Gunicorn command
gunicorn gestion_budget.wsgi:application --bind 0.0.0.0:8001
