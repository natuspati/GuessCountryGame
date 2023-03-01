from datetime import timedelta
from celery import shared_task
from django.utils import timezone
from django.conf import settings
from django.core import management

from custom_auth.models import User


@shared_task(name='remove_inactive')
def remove_inactive_users():
    User.objects.filter(
        is_active=False,
        date_joined=timezone.now() - timedelta(days=settings.ACCOUNT_ACTIVATION_DAYS)
    ).delete()


@shared_task(name='clear_sessions')
def clear_sessions():
    management.call_command("clearsessions", verbosity=0)
