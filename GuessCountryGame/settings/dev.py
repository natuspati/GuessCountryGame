from GuessCountryGame.settings.base import *

SECRET_KEY = 'django-insecure-#9zn3+%yq)8(y)(_@pllkrw@$1hv+j0$=q#-gncasnh*+%fg_1'
DEBUG = values.BooleanValue(True)
ALLOWED_HOSTS = ['*']

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

INTERNAL_IPS = (
    '127.0.0.1',
    '0.0.0.0',
)
