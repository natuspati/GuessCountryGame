from django.dispatch import receiver
from django.db.models.signals import post_save
from django.templatetags.static import static

from allauth.socialaccount.signals import pre_social_login

from custom_auth.models import User
from GuessCountry.models import Score, Note


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
