from GuessCountryGame.settings.base import *

SECRET_KEY = env.str('DJANGO_SECRET_KEY')
DEBUG = False
ALLOWED_HOSTS = env.list('DJANGO_ALLOWED_HOSTS')

# Do not propagate same log in production setting
LOGGING['loggers']['GuessCountry']['propagate'] = False

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = env.str('DJANGO_EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env.str('DJANGO_EMAIL_HOST_PASSWORD')
SERVER_EMAIL = env.str('DJANGO_SERVER_EMAIL')

# Use redis with fallback file cache in production settings
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

# Transfer protocol security settings
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True
