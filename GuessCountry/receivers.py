from django.dispatch import receiver
from django.db.models.signals import post_save

from allauth.socialaccount.signals import pre_social_login

from custom_auth.models import User
from GuessCountry.models import Note

from GuessCountry.signals import daily_game_finished
from GuessCountry.models import Country, Score, UserCountryRecord

import logging

logger = logging.getLogger(__name__)


@receiver(daily_game_finished)
def update_user_score(sender, score, country, success, **kwargs):
    user_country_record, created = UserCountryRecord.objects.update_or_create(
        country=country,
        user_score=score,
        guessed=success
    )
    
    if success:
        score.value += 1
        score.save()
    
    logger.info('{}'.format(user_country_record.__str__()))
    print('SIGNAL RECEIVED!')


# Create user score upon saving
@receiver(post_save, sender=User)
def create_score(sender, instance, created, **kwargs):
    if created:
        Score.objects.create(
            user=instance,
        )
    else:
        instance.score.save()


# Create a note that user used social login to authenticate
@receiver(pre_social_login)
def create_note_social_login(sender, request, sociallogin, **kwargs):
    noted_user = User.objects.filter(email=sociallogin.account.extra_data['email']).first()
    note = Note(
        creator=User.objects.first(),
        content='{} logged in using {}'.format(noted_user, sociallogin.account.provider),
        content_object=noted_user,
    )
    note.save()
