import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'GuessCountryGame.settings.dev')

app = Celery('GuessCountry')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'remove-inactive-users-weekly': {
        'task': 'remove_inactive',
        'schedule': crontab(hour=0, minute=0, day_of_week="sunday"),
    },
    'session-cleanup': {
        'task': 'clear_sessions',
        'schedule': crontab(hour=0, minute=0, day_of_week="sunday"),
    },
    'debug-task': {
        'task': 'debug_task',
        'schedule': 10.0,
    },
}
