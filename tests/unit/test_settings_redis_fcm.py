import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

pytestmark = pytest.mark.django_db  # shared autouse fixtures in conftest.py clean DB tables

BASE_DIR = Path(__file__).resolve().parents[2]

PROBE = (
    "import json, django.conf as c; s = c.settings; "
    "print(json.dumps({'cache': s.CACHES['default']['LOCATION'], 'broker': s.CELERY_BROKER_URL, "
    "'fcm': str(s.PUSH_NOTIFICATIONS_FCM_CREDENTIALS_PATH)}))"
)


def _load_settings(**overrides: str) -> dict[str, str]:
    env = {k: v for k, v in os.environ.items() if not k.startswith(("REDIS_", "PUSH_NOTIFICATIONS_"))}
    env["DJANGO_SETTINGS_MODULE"] = "lacra.settings"
    env.update(overrides)
    result = subprocess.run(
        [sys.executable, "-c", PROBE], cwd=BASE_DIR, env=env, capture_output=True, text=True, check=True
    )
    return json.loads(result.stdout.strip().splitlines()[-1])


@pytest.mark.parametrize(
    ("overrides", "expected"),
    [
        ({}, "redis://127.0.0.1:6379/0"),
        ({"REDIS_HOST": "redis", "REDIS_PASSWORD": "p@ss/w:rd"}, "redis://:p%40ss%2Fw%3Ard@redis:6379/0"),
        (
            {"REDIS_URL": "rediss://user:secret@host:6380/2", "REDIS_HOST": "ignored", "REDIS_PASSWORD": "ignored"},
            "rediss://user:secret@host:6380/2",
        ),
    ],
)
def test_redis_url_is_shared_by_cache_and_celery(overrides: dict[str, str], expected: str) -> None:
    loaded = _load_settings(**overrides)

    assert loaded["cache"] == expected
    assert loaded["broker"] == expected


def test_fcm_credentials_path_default_and_override() -> None:
    assert _load_settings()["fcm"] == str(BASE_DIR / "config" / "push" / "fcm.json")
    overridden = _load_settings(PUSH_NOTIFICATIONS_FCM_CREDENTIALS_PATH="/etc/secrets/fcm.json")

    assert overridden["fcm"] == "/etc/secrets/fcm.json"
