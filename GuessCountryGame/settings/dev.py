from GuessCountryGame.settings.base import *

SECRET_KEY = 'django-insecure-#9zn3+%yq)8(y)(_@pllkrw@$1hv+j0$=q#-gncasnh*+%fg_1'
DEBUG = True
ALLOWED_HOSTS = ['*']

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'my_cache_table',
    }
}

INTERNAL_IPS = (
    '127.0.0.1',
    '0.0.0.0',
)
