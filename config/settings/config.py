import sys

import decouple
import sentry_sdk

from .common import *

DEBUG = decouple.config("DEBUG", default=False, cast=bool)

# Enable restriction to access debug tools like swagger, django debug toolbars,
# Admin page for non-local envs
RESTRICT_DEBUG_ACCESS = True

ENVIRONMENT = decouple.config("ENVIRONMENT")

FRONTEND_URL = decouple.config("FRONTEND_URL", default="")

DATABASES["default"].update(
    NAME=decouple.config("RDS_DB_NAME"),
    USER=decouple.config("RDS_DB_USER"),
    PASSWORD=decouple.config("RDS_DB_PASSWORD"),
    HOST=decouple.config("RDS_DB_HOST"),
    PORT=decouple.config("RDS_DB_PORT"),
)

AWS_STORAGE_BUCKET_NAME = decouple.config("AWS_S3_BUCKET_NAME")
AWS_S3_REGION_NAME = decouple.config("AWS_S3_DIRECT_REGION")
AWS_S3_ENDPOINT_URL = f"https://s3.{AWS_S3_REGION_NAME}.amazonaws.com"

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_UI_URL = decouple.config("EMAIL_UI_URL")
EMAIL_HOST = decouple.config("EMAIL_HOST")
EMAIL_HOST_USER = decouple.config("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = decouple.config("EMAIL_HOST_PASSWORD")
EMAIL_PORT = decouple.config("EMAIL_HOST_PORT", cast=int)
EMAIL_USE_TLS = decouple.config("EMAIL_HOST_USE_TLS", cast=bool)
DEFAULT_FROM_EMAIL = (
    decouple.config("DEFAULT_FROM_EMAIL") or "no-reply@bika.com"
)

redis_host = decouple.config("REDIS_HOST")
redis_port = decouple.config("REDIS_PORT", cast=int)
redis_db = decouple.config("REDIS_DB", cast=int)

CELERY_TASK_DEFAULT_QUEUE = (
    f"{APP_LABEL.lower().replace(' ', '-')}-{ENVIRONMENT}"
)
CELERY_BROKER_URL = f"redis://{redis_host}:{redis_port}/{redis_db}"
CELERY_RESULT_BACKEND = f"redis://{redis_host}:{redis_port}/{redis_db}"

# Setting needed for redis health check
REDIS_URL = f"redis://{redis_host}:{redis_port}/{redis_db}"

CACHES["default"].update(
    LOCATION=REDIS_URL,
)
# https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
SECRET_KEY = decouple.config("DJANGO_SECRET_KEY")
ALLOWED_HOSTS = ["*"]

# disable django DEBUG if we run celery worker
if "celery" in sys.argv[0]:
    DEBUG = False

if DEBUG:
    # Dev tools settings
    from .common.dev_tools import *


# Start up sentry
sentry_sdk.init(
    dsn=decouple.config("SENTRY_DSN"),
    environment=ENVIRONMENT,
    **SENTRY_CONFIG,
)
