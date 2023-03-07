from GuessCountryGame.settings.base import *

SECRET_KEY = 'django-insecure-#9zn3+%yq)8(y)(_@pllkrw@$1hv+j0$=q#-gncasnh*+%fg_1'
DEBUG = True
ALLOWED_HOSTS = ['*']

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

DATABASES = {
    'default': dj_database_url.config(default=f'sqlite:///{BASE_DIR}/example-db.sqlite3'),
}

# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
#     }
# }

# Use cached version after finishing testing redis caching
CACHES = {
    'default': {
        'BACKEND': 'cache_fallback.FallbackCache',
    },
    'main_cache': {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    },
    'fallback_cache': {
        'BACKEND':
            'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': BASE_DIR / 'var/django_cache',
    },
}


INTERNAL_IPS = (
    '127.0.0.1',
    '0.0.0.0',
)
