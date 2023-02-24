from datetime import timedelta
from celery import shared_task
from django.utils import timezone
from django.conf import settings

from custom_auth.models import User


@shared_task(name='remove_inactive')
def remove_inactive_users():
    User.objects.filter(
        is_active=False,
        date_joined=timezone.now() - timedelta(days=settings.ACCOUNT_ACTIVATION_DAYS)
    ).delete()
