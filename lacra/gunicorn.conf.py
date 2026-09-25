import os
from multiprocessing import cpu_count

# Render sets $PORT to 10000 for Docker web services.
# Fall back to 8000 for local development.
port = os.environ.get("PORT", "8000")
bind = f"0.0.0.0:{port}"

# Respect WEB_CONCURRENCY env var (set by Render/Heroku).
# Default to 2 workers to stay within 512MB free-tier RAM.
# Never exceed cpu_count * 2 + 1.
_default_workers = min(2, cpu_count() * 2 + 1)
workers = int(os.environ.get("WEB_CONCURRENCY", _default_workers))
