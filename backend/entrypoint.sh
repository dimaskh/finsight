#!/bin/bash

# Wait for PostgreSQL
echo "Waiting for PostgreSQL..."
while ! nc -z finsight-db 5432; do
  sleep 0.1
done
echo "PostgreSQL started"

# Wait for Redis
echo "Waiting for Redis..."
while ! nc -z finsight-redis 6379; do
  sleep 0.1
done
echo "Redis started"

# Create migrations
echo "Creating migrations..."
python manage.py makemigrations

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate

# Create superuser if it doesn't exist
echo "Creating superuser..."
python manage.py shell -c "
from django.contrib.auth import get_user_model;
User = get_user_model();
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin')
"

# Start Celery worker
celery -A config worker --loglevel=info &

# Start Celery beat
celery -A config beat --loglevel=info &

# Start Gunicorn
echo "Starting Gunicorn..."
gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 4 --threads 4 --timeout 120
