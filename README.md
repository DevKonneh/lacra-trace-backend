[![Swagger](https://img.shields.io/badge/-Swagger-%23Clojure?style=for-the-badge&logo=swagger&logoColor=white)](docs/openapi.yaml)

# 🌱️ LACRA Trace

LACRA Trace REST API backend service (Liberia Agriculture Commodity Regulatory Authority)

## 🛠️ Tech Stack

### 📋 Requirements

- 🐳 [Docker](https://docs.docker.com/) - Platform for developing, shipping, and running applications in containers
- 📦 [Docker Compose](https://docs.docker.com/compose/) - Tool for defining and running multi-container applications
- 🐍 [Python 3.12](https://docs.python.org/3.12/) - High-level programming language with a focus on code readability
- 🔨 [uv 0.7.6](https://docs.astral.sh/uv/) - Fast Python package installer and resolver

### 🦾 Main Stack

- 🌐 [Django 5.2](https://docs.djangoproject.com/en/5.2/) - High-level web framework that encourages rapid development
- 🔌 [Django REST Framework 3.16+](https://www.django-rest-framework.org/) - Toolkit for building Web APIs in Django
- 🚀 [Gunicorn 23+](https://gunicorn.org/) - Python WSGI HTTP Server for UNIX
- 🐘 [PostgreSQL 17](https://www.postgresql.org/docs/) - Powerful, open source object-relational database
- ✅ [Pydantic 2.11+](https://docs.pydantic.dev/) - Data validation and settings management using Python type annotations
- 🗄️ [Redis 7](https://redis.io/docs/) - In-memory data structure store used for caching

### ⚙️ Development Tools

- 🏭 [Factory Boy 3.3+](https://factoryboy.readthedocs.io/) - Fixture replacement for testing
- 🔍 [Mypy 1.15+](https://mypy.readthedocs.io/) - Static type checker for Python
- 📋 [OpenAPI Spec Validator 0.7+](https://github.com/p1c2u/openapi-spec-validator) - OpenAPI Specification validator
- 🧪 [Pytest 8.3+](https://docs.pytest.org/) - Testing framework for Python
- ✨ [Ruff 0.11+](https://docs.astral.sh/ruff/) - Fast Python linter and formatter
- 🔄 [Tox 4.25+](https://tox.wiki/en/latest/) - Tool for automating testing in multiple environments

## 🏗 Local Setup

### ✍️ Create environment file

Create a new configuration directory and copy the sample environment file:

```bash
cp config/env.sample config/.env
```

Edit the configuration values in `config/.env` as needed for your environment.

### 🔥 Place Firebase credentials

Place the Firebase service-account JSON in `config/push/fcm.json` (or set `PUSH_NOTIFICATIONS_FCM_CREDENTIALS_PATH`) and set `PUSH_NOTIFICATIONS_FCM_ENABLED=True`

### 🚀 Start the services

```bash
docker compose -f deploy/docker-compose.yaml up -d
```

### 🔭 Access the services

- 🌐 API: http://127.0.0.1:8000/api/v1/
- 💼 Admin panel: http://127.0.0.1:8000/admin/
- 📚 API documentation: http://127.0.0.1:8000/docs/

## 🇱🇷 LACRA deployment notes

This repository is the LACRA Trace backend, derived from the EFI `whimo-backend` (MIT, Copyright (c) 2025 EFI https://efi.int/ - see `LICENSE`).
It serves the **LACRA Trace** Android app (`lr.gov.lacra.trace`). The API contract is unchanged from upstream.

### Verified locally

- `pytest tests`: 760 passed (Postgres 17 + Redis, 412 snapshots matched).
- `migrate` + `migrate --database=test_mode`, `createsuperuser`, `collectstatic` and `gunicorn` start cleanly.
- Smoke-tested over HTTP: healthcheck, registration, JWT login, profile, commodity groups, balances, `harvest-seasons/`, transactions, notifications, admin login page (LACRA branding).

### Deploying on Render

`render.yaml` is a pilot-grade Blueprint: dedicated PostgreSQL (`lacra-trace-pg`), Key Value (`lacra-trace-kv`), web service
(`lacra-trace`) and a Celery worker+beat service (`lacra-trace-worker`). Every secret is `sync: false` (entered in the Render
dashboard; nothing is committed). The full runbook, exact environment-variable table, Firebase/Telnyx/SMTP/S3 steps and the
database-migration notes are in [`docs/RENDER_DEPLOY.md`](docs/RENDER_DEPLOY.md).

Key facts:

- OTP codes live in Redis and are sent by Celery (`send_sms`/`send_email`), so the **worker and Key Value are mandatory**.
- Redis is configured with `REDIS_URL` (Render connection string) or, as before, `REDIS_HOST`/`REDIS_PORT`/`REDIS_PASSWORD` (password optional).
- Firebase credentials: `PUSH_NOTIFICATIONS_FCM_CREDENTIALS_PATH` (default `config/push/fcm.json`; on Render a Secret File at `/etc/secrets/fcm.json`).
- Static files (admin CSS) are served by WhiteNoise.
- The Android app's `BASE_URL` must be `https://<your-host>/api/v1/` and `TEST_BASE_URL` `https://<your-host>/api/v1/test/`.

### Checks run before this PR

`ruff check`, `ruff format --check`, `mypy` (312 files), `openapi-spec-validator docs/openapi.yaml` and `pytest tests` (see the PR description for results).

## 🚧 Development

### 🛠️ Code Quality Tools

#### ✅ Run all checks

```bash
uv run tox
```

#### ✨ Format code

```bash
uv run tox -e format
```

#### 🔍 Lint code

```bash
uv run tox -e lint,typing,openapi
```

#### 🧪 Run tests

```bash
uv run tox -e test
```

### 🌐 Internationalization

#### 📤 Extract messages for translation

```bash
uv run manage.py makemessages --all
```

#### ⚙️ Compile translation files

```bash
uv run manage.py compilemessages
```
