from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from django.db.models.signals import post_save
from django.dispatch import receiver


def _avatar_path(instance, filename):
    return 'avatars/{}.{}'.format(instance.user.id, filename.split('.')[-1])


class Details(models.Model):
    """Stores the data about user which can't be stored anywhere else."""

    GENDER_CHOICES = (
        (None, _('unknown')),
        (True, _('male')),
        (False, _('female'))
    )
    UNIT_CHOICES = (
        (True, _('Metric (kilometers, kilograms)')),
        (False, _('Imperial (miles, pounds)'))
    )

    user = models.OneToOneField(User)

    gender = models.NullBooleanField(_('gender'), choices=GENDER_CHOICES, default=None)
    si_units = models.BooleanField(_('units'), choices=UNIT_CHOICES, default=True)

    avatar = models.ImageField(_('avatar'), upload_to=_avatar_path, null=True)


@receiver(post_save, sender=User)
def create_related(sender, **kwargs):
    """Creates Details object upon the creation of an user."""

    if kwargs.get('created', False):
        Details.objects.get_or_create(user=kwargs.get('instance'))
