#!/bin/bash

echo "Apply database migrations"
uv run --no-dev ./manage.py migrate

echo "Create superuser"
uv run --no-dev ./manage.py createsuperuser --noinput

echo "Collect static files"
uv run --no-dev ./manage.py collectstatic --noinput

# compilemessages skipped — takes 10+ minutes scanning Django locale files

echo "Start gunicorn server on port ${PORT:-8000}"
uv run --no-dev gunicorn \
    --bind "0.0.0.0:${PORT:-8000}" \
    --workers "${WEB_CONCURRENCY:-2}" \
    --timeout 120 \
    lacra.common.wsgi

exec "$@"
