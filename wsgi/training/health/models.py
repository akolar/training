from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from django.db.models.signals import post_save
from django.dispatch import receiver


class Athlete(models.Model):
    user = models.OneToOneField(User)

    resting_hr = models.IntegerField(_('resting hear rate'), null=True, blank=True)
    max_hr = models.IntegerField(_('maximum heart rate'), null=True, blank=True)
    lt_hr = models.IntegerField(_('lactate threshold heart rate'), null=True, blank=True)

    max_power = models.IntegerField(_('maximum power'), null=True, blank=True)
    lt_power = models.IntegerField(_('functional threshold power'), null=True, blank=True)

    height = models.IntegerField(_('height'), null=True, blank=True)


@receiver(post_save, sender=User)
def create_related(sender, **kwargs):
    if kwargs.get('created', False):
        Athlete.objects.get_or_create(user=kwargs.get('instance'))
