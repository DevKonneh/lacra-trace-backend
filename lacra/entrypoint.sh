#!/bin/bash

echo "Apply database migrations"
uv run --no-dev ./manage.py migrate

echo "Create superuser"
uv run --no-dev ./manage.py createsuperuser --noinput

echo "Collect static files"
uv run --no-dev ./manage.py collectstatic --noinput

# compilemessages is skipped at runtime — it scans all Django locale files
# and takes 10+ minutes on the free tier, causing health check timeouts.
# Run it locally or in a build step if needed.

echo "Start gunicorn server"
uv run --no-dev gunicorn -c ./lacra/gunicorn.conf.py lacra.common.wsgi

exec "$@"
