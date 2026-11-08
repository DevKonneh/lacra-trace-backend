from datetime import timedelta
from pathlib import Path
from urllib.parse import quote

import environ
import firebase_admin
import sentry_sdk
from django.templatetags.static import static
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from sentry_sdk.integrations.celery import CeleryIntegration
from sentry_sdk.integrations.django import DjangoIntegration

env = environ.Env()

_not_set = object()

# Django
# ______________________________________________________________________________________________________________________

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = env.str("DJANGO_SECRET_KEY")

DEBUG = env.bool("DJANGO_DEBUG", default=False)

ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS", default=())

CORS_ALLOWED_ORIGINS = env.list("DJANGO_CORS_ALLOWED_ORIGINS", default=())

CSRF_TRUSTED_ORIGINS = env.list("DJANGO_CSRF_TRUSTED_ORIGINS", default=())

INSTALLED_APPS = (
    # unfold admin
    "unfold",
    "unfold.contrib.simple_history",
    "unfold.contrib.filters",
    "unfold.contrib.forms",
    "unfold.contrib.inlines",
    "unfold.contrib.import_export",
    # django core
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.humanize",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # third party apps
    "constance",
    "corsheaders",
    "import_export",
    "rest_framework",
    "rest_framework_simplejwt",
    "simple_history",
    "django_celery_beat",
    "django_celery_results",
    "push_notifications",
    # project apps
    "lacra.db",
    "lacra.analytics",
    "lacra.auth.jwt",
    "lacra.auth.otp",
    "lacra.auth.registration",
    "lacra.auth.social",
    "lacra.commodities",
    "lacra.common",
    "lacra.contrib",
    "lacra.harvest_seasons",
    "lacra.notifications",
    "lacra.system",
    "lacra.transactions",
    "lacra.users",
)

MIDDLEWARE = (
    "lacra.common.middleware.TestModeMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "simple_history.middleware.HistoryRequestMiddleware",
)

ROOT_URLCONF = "lacra.urls"

TEMPLATES = (
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": (BASE_DIR / "lacra" / "contrib" / "templates",),
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": (
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ),
        },
    },
)

CONSTANCE_BACKEND = "constance.backends.database.DatabaseBackend"

WSGI_APPLICATION = "lacra.common.wsgi.application"

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": ("lacra.common.authentication.JWTAuthentication",),
    "DEFAULT_PERMISSION_CLASSES": ("lacra.common.authentication.HasVerifiedGadgetPermission",),
    "DEFAULT_THROTTLE_CLASSES": [
        "lacra.common.throttling.DefaultUserThrottle",
        "lacra.common.throttling.DefaultAnonThrottle",
    ],
    "DEFAULT_THROTTLE_RATES": {
        "anon": "100/hour",
        "user": "1000/hour",
        "otp": "5/minute",
        "otp_identifier_cooldown": "1/minute",
        "otp_identifier": "5/hour",
        "auth": "20/minute",
        "downloads": "10/hour",
    },
    "EXCEPTION_HANDLER": "lacra.common.views.custom_exception_handler",
}

# Logging
# ______________________________________________________________________________________________________________________

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "level": env.str("DJANGO_LOG_LEVEL", default="INFO"),
            "filters": None,
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": env.str("DJANGO_LOG_LEVEL", default="INFO"),
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": env.str("DJANGO_LOG_LEVEL", default="INFO"),
        },
    },
}

# Sentry
# ______________________________________________________________________________________________________________________

SENTRY_DSN = env.str("SENTRY_DSN", default="")

SENTRY_ENVIRONMENT = env.str("SENTRY_ENVIRONMENT", default="production")

sentry_sdk.init(
    dsn=SENTRY_DSN,
    send_default_pii=True,
    environment=SENTRY_ENVIRONMENT,
    traces_sample_rate=1.0,
    profile_session_sample_rate=1.0,
    profile_lifecycle="trace",
    integrations=[
        DjangoIntegration(),
        CeleryIntegration(monitor_beat_tasks=True),
    ],
    _experiments={
        "enable_logs": True,
    },
)

# Databases
# ______________________________________________________________________________________________________________________

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "HOST": env.str("POSTGRES_HOST", default="127.0.0.1"),
        "PORT": env.int("POSTGRES_PORT", default=5432),
        "USER": env.str("POSTGRES_USER", default="app"),
        "PASSWORD": env.str("POSTGRES_PASSWORD"),
        "NAME": env.str("POSTGRES_DB", default="app"),
    },
    "test_mode": {
        "ENGINE": "django.db.backends.postgresql",
        "HOST": env.str("POSTGRES_HOST", default="127.0.0.1"),
        "PORT": env.int("POSTGRES_PORT", default=5432),
        "USER": env.str("POSTGRES_USER", default="app"),
        "PASSWORD": env.str("POSTGRES_PASSWORD"),
        "NAME": env.str("POSTGRES_DB", default="app"),
        "OPTIONS": {"options": "-c search_path=test_mode,public"},
        # Same physical database as "default" - don't let the test runner create a
        # second physical test database for this alias.
        "TEST": {"MIRROR": "default"},
    },
}

DATABASE_ROUTERS = ["lacra.common.db_router.TestModeRouter"]

# Caching
# ______________________________________________________________________________________________________________________

REDIS_HOST = env.str("REDIS_HOST", default="127.0.0.1")

REDIS_PORT = env.int("REDIS_PORT", default=6379)

REDIS_DB = env.int("REDIS_DB", default=0)

# Optional: managed Redis/Key Value services (e.g. Render) hand out a single connection string. When REDIS_URL is
# set it wins over REDIS_HOST/REDIS_PORT/REDIS_DB/REDIS_PASSWORD. Use the ``rediss://`` scheme for TLS endpoints.
# REDIS_PASSWORD stays supported for the original compose setup and may be empty for password-less internal Redis.
REDIS_PASSWORD = env.str("REDIS_PASSWORD", default="")

REDIS_URL = env.str("REDIS_URL", default="") or (
    f"redis://:{quote(REDIS_PASSWORD, safe='')}@{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}"
    if REDIS_PASSWORD
    else f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}"
)

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": REDIS_URL,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    },
}

# Celery
# ----------------------------------------------------------------------------------------------------------------------

CELERY_BROKER_URL = REDIS_URL

CELERY_RESULT_BACKEND = "django-db"

CELERY_CACHE_BACKEND = "django-cache"

CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"

# Storages
# ______________________________________________________________________________________________________________________

S3_OPTIONS = {
    "endpoint_url": env.str("S3_ENDPOINT_URL", default=_not_set),
    "region_name": env.str("S3_REGION", default=_not_set),
    "bucket_name": env.str("S3_BUCKET_NAME", default=_not_set),
    "access_key": env.str("S3_ACCESS_KEY", default=_not_set),
    "secret_key": env.str("S3_SECRET_KEY", default=_not_set),
}

S3_OPTIONS = {option: value for option, value in S3_OPTIONS.items() if value is not _not_set}

STORAGES = {
    "default": {
        "BACKEND": "storages.backends.s3.S3Storage",
        "OPTIONS": S3_OPTIONS,
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
    },
}

# Security
# ______________________________________________________________________________________________________________________

OTP_LENGTH = env.int("OTP_LENGTH", default=6)

OTP_EXPIRY_MINUTES = env.int("OTP_EXPIRY_MINUTES", default=15)

OTP_MOCK_CODE = env.str("OTP_MOCK_CODE", default=None)

AUTH_USER_MODEL = "db.User"

AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    "lacra.common.authentication.GadgetsModelBackend",
)

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(hours=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
}

AUTH_PASSWORD_VALIDATORS = ()

# OAuth
# ______________________________________________________________________________________________________________________

OAUTH_GOOGLE_CLIENT_ID = env.str("OAUTH_GOOGLE_CLIENT_ID", default="")

OAUTH_GOOGLE_CLIENT_SECRET = env.str("OAUTH_GOOGLE_CLIENT_SECRET", default="")

OAUTH_APPLE_CLIENT_ID = env.str("OAUTH_APPLE_CLIENT_ID", default="")

OAUTH_APPLE_CLIENT_SECRET = env.str("OAUTH_APPLE_CLIENT_SECRET", default="")

# Email
# ______________________________________________________________________________________________________________________

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

EMAIL_HOST = env.str("EMAIL_HOST", default="localhost")

EMAIL_PORT = env.int("EMAIL_PORT", default=25)

EMAIL_HOST_USER = env.str("EMAIL_HOST_USER", default="lacra")

EMAIL_HOST_PASSWORD = env.str("EMAIL_HOST_PASSWORD")

DEFAULT_FROM_EMAIL = env.str("DEFAULT_FROM_EMAIL", default=EMAIL_HOST_USER)

EMAIL_USE_TLS = env.bool("EMAIL_USE_TLS", default=True)

# SMS
# ______________________________________________________________________________________________________________________

SMS_TELNYX_API_KEY = env.str("SMS_TELNYX_API_KEY")

SMS_TELNYX_SENDER_ID = env.str("SMS_TELNYX_SENDER_ID")

SMS_TELNYX_MESSAGING_PROFILE_ID = env.str("SMS_TELNYX_MESSAGING_PROFILE_ID")

# Captcha
# ______________________________________________________________________________________________________________________

CAPTCHA_TURNSTILE_SECRET_KEY = env.str("CAPTCHA_TURNSTILE_SECRET_KEY", default="")

# Firebase
# ______________________________________________________________________________________________________________________

PUSH_NOTIFICATIONS_CONFIG_PATH = BASE_DIR / "config" / "push"

# Path of the Firebase service-account JSON. Defaults to config/push/fcm.json (docker volume); on Render upload it as a
# Secret File and set this to /etc/secrets/fcm.json.
PUSH_NOTIFICATIONS_FCM_CREDENTIALS_PATH = Path(
    env.str("PUSH_NOTIFICATIONS_FCM_CREDENTIALS_PATH", default=str(PUSH_NOTIFICATIONS_CONFIG_PATH / "fcm.json"))
)

PUSH_NOTIFICATIONS_SETTINGS_FCM_APP_ID = env.str("PUSH_NOTIFICATIONS_FCM_APP_ID", default="fcm")

PUSH_NOTIFICATIONS_SETTINGS_APNS_APP_ID = env.str("PUSH_NOTIFICATIONS_APNS_APP_ID", default="apns")

PUSH_NOTIFICATIONS_SETTINGS = {
    "CONFIG": "push_notifications.conf.AppConfig",
    "USER_MODEL": AUTH_USER_MODEL,
    "APPLICATIONS": {},
}

if env.bool("PUSH_NOTIFICATIONS_FCM_ENABLED", default=False):  # pragma: no cover
    PUSH_NOTIFICATIONS_SETTINGS["APPLICATIONS"][PUSH_NOTIFICATIONS_SETTINGS_FCM_APP_ID] = {  # type: ignore
        "PLATFORM": "FCM",
        "FIREBASE_APP": firebase_admin.initialize_app(
            credential=firebase_admin.credentials.Certificate(PUSH_NOTIFICATIONS_FCM_CREDENTIALS_PATH),
        ),
    }

if env.bool("PUSH_NOTIFICATIONS_APNS_ENABLED", default=False):  # pragma: no cover
    PUSH_NOTIFICATIONS_SETTINGS["APPLICATIONS"][PUSH_NOTIFICATIONS_SETTINGS_APNS_APP_ID] = {  # type: ignore
        "PLATFORM": "APNS",
        "CERTIFICATE": str(PUSH_NOTIFICATIONS_CONFIG_PATH / "apns.pem"),
        "USE_SANDBOX": env.bool("PUSH_NOTIFICATIONS_APNS_USE_SANDBOX", default=False),
    }

# Localization
# ______________________________________________________________________________________________________________________

LANGUAGE_CODE = "en-US"

LANGUAGES = (
    ("en-US", "English"),
    ("fr-FR", "French"),
    ("es-ES", "Spanish"),
)

LOCALE_PATHS = (BASE_DIR / "locale",)

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

# Static files
# ______________________________________________________________________________________________________________________

STATIC_URL = "static/"

STATIC_ROOT = BASE_DIR / "static"

# Proxy
# ______________________________________________________________________________________________________________________

USE_X_FORWARDED_HOST = env.bool("DJANGO_USE_X_FORWARDED_HOST", False)

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", env.str("DJANGO_HTTP_X_FORWARDED_PROTO", "http"))

# Misc
# ______________________________________________________________________________________________________________________

LACRA_TRANSACTION_EXPIRATION_DAYS = env.int("LACRA_TRANSACTION_EXPIRATION_DAYS", default=30)

# Django Admin
# ______________________________________________________________________________________________________________________

UNFOLD = {
    "SITE_TITLE": "LACRA Trace Admin",
    "SITE_HEADER": "LACRA Trace Administration",
    "SITE_SUBHEADER": "Liberia Agriculture Commodity Regulatory Authority",
    "SITE_URL": "/",
    # Official LACRA logo on a white disc (lacra/contrib/static/lacra/). Derived from a 512px JPEG.
    "SITE_ICON": lambda _request: static("lacra/logo.png"),
    "SITE_FAVICONS": [
        {"rel": "icon", "sizes": "64x64", "type": "image/png", "href": lambda _request: static("lacra/favicon.png")},
    ],
    # Primary colour scale built from the brand green #226C13 (600), which is derived from the logo.
    "COLORS": {
        "primary": {
            "50": "240, 245, 238",
            "100": "222, 233, 220",
            "200": "189, 211, 184",
            "300": "149, 184, 142",
            "400": "100, 152, 90",
            "500": "61, 126, 47",
            "600": "34, 108, 19",
            "700": "28, 89, 16",
            "800": "22, 71, 13",
            "900": "18, 56, 10",
            "950": "11, 35, 6",
        },
    },
    "DASHBOARD_CALLBACK": "lacra.contrib.admin.dashboard.dashboard_callback",
    "SIDEBAR": {
        "show_search": True,
        "show_all_applications": True,
        "navigation": [
            {
                "title": _("Navigation"),
                "separator": True,
                "items": [
                    {
                        "title": _("Dashboard"),
                        "icon": "dashboard",
                        "link": reverse_lazy("admin:index"),
                    },
                    {
                        "title": _("Periodic Tasks"),
                        "icon": "task",
                        "link": reverse_lazy("admin:django_celery_beat_periodictask_changelist"),
                    },
                ],
            },
            {
                "title": _("User Management"),
                "separator": True,
                "items": [
                    {
                        "title": _("Users"),
                        "icon": "person",
                        "link": reverse_lazy("admin:db_user_changelist"),
                    },
                    {
                        "title": _("Gadgets"),
                        "icon": "devices",
                        "link": reverse_lazy("admin:db_gadget_changelist"),
                    },
                    {
                        "title": _("Notifications"),
                        "icon": "notifications",
                        "link": reverse_lazy("admin:db_notification_changelist"),
                    },
                ],
            },
            {
                "title": _("Commodities"),
                "separator": True,
                "items": [
                    {
                        "title": _("Commodity Groups"),
                        "icon": "category",
                        "link": reverse_lazy("admin:db_commoditygroup_changelist"),
                    },
                    {
                        "title": _("Commodities"),
                        "icon": "inventory",
                        "link": reverse_lazy("admin:db_commodity_changelist"),
                    },
                    {
                        "title": _("Conversion Recipes"),
                        "icon": "transform",
                        "link": reverse_lazy("admin:db_conversionrecipe_changelist"),
                    },
                    {
                        "title": _("Harvest Seasons"),
                        "icon": "calendar_month",
                        "link": reverse_lazy("admin:db_harvestseason_changelist"),
                    },
                ],
            },
            {
                "title": _("Trading"),
                "separator": True,
                "items": [
                    {
                        "title": _("Transactions"),
                        "icon": "swap_horiz",
                        "link": reverse_lazy("admin:db_transaction_changelist"),
                    },
                    {
                        "title": _("Balances"),
                        "icon": "account_balance",
                        "link": reverse_lazy("admin:db_balance_changelist"),
                    },
                ],
            },
        ],
    },
}
