"""
ASGI config for GuessCountryGame project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
# from configurations.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'GuessCountryGame.settings.prod')
# os.environ.setdefault('DJANGO_CONFIGURATION', 'Prod')

application = get_asgi_application()
