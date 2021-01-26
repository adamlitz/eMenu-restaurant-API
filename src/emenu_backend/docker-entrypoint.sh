#!/usr/bin/env sh

# Collect static files
echo "Collect static files"
python manage.py collectstatic --noinput

# Apply database migrations
echo "Apply database migrations"
python manage.py migrate

# wait for postgres
./wait_for_postgres.sh

# Run development server
python manage.py runserver 0.0.0.0:8000