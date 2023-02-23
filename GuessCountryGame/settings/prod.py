from GuessCountryGame.settings.base import *

SECRET_KEY = values.SecretValue()
DEBUG = values.BooleanValue(False)
ALLOWED_HOSTS = values.ListValue(['localhost', '0.0.0.0'])

# Do not propagate same log in production setting
LOGGING['loggers']['GuessCountry']['propagate'] = False

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = values.SecretValue()
EMAIL_HOST_PASSWORD = values.SecretValue()
SERVER_EMAIL = values.SecretValue()

# Use memcached with fallback file cache in production settings
CACHES = {
    'default': {
        'BACKEND': 'cache_fallback.FallbackCache',
    },
    
    'main_cache': {
        'BACKEND': 'django.core.cache.backends.memcached.PyMemcacheCache',
        'LOCATION': '/var/memcached.sock',
        'TIMEOUT': 600,
    },
    'fallback_cache': {
        'BACKEND':
            'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': '/var/django_cache',
        'TIMEOUT': 600,
    },
}

# Transfer protocol security settings
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True