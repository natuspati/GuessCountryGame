from GuessCountryGame.settings.base import *

SECRET_KEY = 'django-insecure-#9zn3+%yq)8(y)(_@pllkrw@$1hv+j0$=q#-gncasnh*+%fg_1'
DEBUG = values.BooleanValue(True)
ALLOWED_HOSTS = ['*']

# Use console for emails in development settings
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

CACHES = {
    'default': {
        'BACKEND':
            'django.core.cache.backends.dummy.DummyCache',
    },
}

INTERNAL_IPS = (
    '127.0.0.1',
    '0.0.0.0',
)