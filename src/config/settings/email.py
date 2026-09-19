from .env import (
    DEFAULT_FROM_EMAIL,
    EMAIL_HOST,
    EMAIL_HOST_PASSWORD,
    EMAIL_HOST_USER,
    EMAIL_PORT,
    EMAIL_USE_SSL,
    EMAIL_USE_TLS,
)

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
