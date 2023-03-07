from datetime import timedelta
from celery import shared_task
from django.utils import timezone
from django.conf import settings
from django.core import management
from django_celery_beat.models import PeriodicTask, IntervalSchedule

from custom_auth.models import User
from GuessCountry.models import Country


@shared_task(name='remove_inactive')
def remove_inactive_users():
    User.objects.filter(
        is_active=False,
        date_joined=timezone.now() - timedelta(days=settings.ACCOUNT_ACTIVATION_DAYS)
    ).delete()


@shared_task(name='clear_sessions')
def clear_sessions():
    management.call_command("clearsessions", verbosity=0)


@shared_task(name='reset_countries')
def reset_countries_dates(create_next=True):
    # Calculate the next date to schedule this task
    today = timezone.now()
    country_set = Country.objects.all().order_by('?')
    number_of_countries = country_set.count()
    
    # Fill out the to be used dates for each country in random order
    for country in country_set:
        today += timedelta(days=1)
        country.to_be_used_at = today
        country.save()
    
    if create_next:
        # Create next Periodic Task to go off only once
        schedule, created = IntervalSchedule.objects.get_or_create(
            every=number_of_countries,
            period=IntervalSchedule.DAYS,
        )
        PeriodicTask.objects.create(
            interval=schedule,
            name='Reset dates, created: {}, next: {}'.format(timezone.now().strftime('%Y/%m/%d'),
                                                             today.strftime('%Y/%m/%d')),
            task='reset_countries',
            one_off=True,
        )
