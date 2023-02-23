from datetime import timedelta
from celery import shared_task
from django.utils import timezone
from django.conf import settings

from custom_auth.models import User


@shared_task(name='print_msg_main')
def print_message(message, *args, **kwargs):
    print(f'Celery is working!! Message is {message}')


@shared_task(name='print_time')
def print_time():
    now = timezone.now()
    current_time = now.strftime('%H:%M:%S')
    print(f'Current Time is {current_time}')


@shared_task(name='remove_inactive')
def remove_not_activated_users():
    User.objects.filter(
        is_active=False,
        date_joined=timezone.now() - timedelta(days=settings.ACCOUNT_ACTIVATION_DAYS)
    ).delete()


@shared_task(name='change_name')
def change_name():
    guest_user = User.objects.filter(email__exact='guest@gmail.com').first()
    if guest_user:
        day_of_month = timezone.now().day
        guest_user.first_name = 'Even' if day_of_month % 2 == 0 else 'Odd'
