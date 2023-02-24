import os
from datetime import timedelta
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'GuessCountryGame.settings.dev')

app = Celery('GuessCountry')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))


app.conf.beat_schedule = {
    'remove-inactive-users-weekly': {
        'task': 'remove_inactive',
        'schedule': timedelta(days=7),
    },
}
