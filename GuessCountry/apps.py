from django.apps import AppConfig


class GuesscountryConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'GuessCountry'
    
    def ready(self):
        import GuessCountry.celery
