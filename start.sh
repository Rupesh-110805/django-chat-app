#!/bin/bash
# Railway start script for Django

# Collect static files
python manage.py collectstatic --noinput

# Apply database migrations
python manage.py migrate

# Start the server
daphne mysite.asgi:application --port $PORT --bind 0.0.0.0 -v2
