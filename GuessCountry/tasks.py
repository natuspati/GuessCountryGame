from celery import shared_task
from django.conf import settings
from django.utils import timezone

from datetime import timedelta

from custom_auth.models import User


@shared_task()
def remove_not_activated_users():
    User.objects.filter(
        is_active=False,
        date_joined=timezone.now() - timedelta(days=settings.ACCOUNT_ACTIVATION_DAYS)
    ).delete()


@shared_task()
def test_fun():
    guest_user = User.objects.filter(email__exact='guest@gmail.com').first()
    if guest_user:
        day_of_month = timezone.now().day
        guest_user.first_name = 'Even' if day_of_month % 2 == 0 else 'Odd'
