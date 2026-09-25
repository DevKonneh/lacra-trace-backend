import os
from multiprocessing import cpu_count

bind = "0.0.0.0:8000"

# Respect WEB_CONCURRENCY env var (set by Render/Heroku).
# Default to 2 workers to stay within 512MB free-tier RAM.
# Never exceed cpu_count * 2 + 1.
_default_workers = min(2, cpu_count() * 2 + 1)
workers = int(os.environ.get("WEB_CONCURRENCY", _default_workers))
