from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from settings.models import Details
from health.models import Athlete


@receiver(post_save, sender=User)
def create_related(sender, **kwargs):
    if kwargs.get('created', False):
        Details.objects.get_or_create(user=kwargs.get('instance'))
        Athlete.objects.get_or_create(user=kwargs.get('instance'))
