from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils.translation import ugettext as _


class Goals(models.Model):
    """Object containing data about goals user has created for himself."""

    user = models.OneToOneField(User)

    weekly_distance = models.IntegerField(_('weekly goal (distance)'), default=0)
    weekly_time = models.IntegerField(_('weekly goal (time)'), default=0)

    monthly_distance = models.IntegerField(_('monthly goal (distance)'), default=0)
    monthly_time = models.IntegerField(_('monthly goal (time)'), default=0)

    yearly_distance = models.IntegerField(_('yearly goal (distance)'), default=0)
    yearly_time = models.IntegerField(_('yearly goal (time)'), default=0)

    def weekly_progress(self, distance=0, time=0):
        """Returns weekly progress percentage.
        Arguments:
            distance: completed distance
            time: time spent
        """

        if distance is None:
            distance = 0
        if time is None:
            time = 0

        dist_progress = distance / float(self.weekly_distance * 1000) if self.weekly_distance else 1
        time_progress = time / float(self.weekly_time * 3600) if self.weekly_time else 1

        return int(round(min(dist_progress, time_progress) * 100, 0))

    def monthly_progress(self, distance=0, time=0):
        """Returns monthly progress percentage.
        Arguments:
            distance: completed distance
            time: time spent
        """

        if distance is None:
            distance = 0
        if time is None:
            time = 0

        dist_progress = distance / float(self.monthly_distance * 1000) if self.monthly_distance else 1
        time_progress = time / float(self.monthly_time * 3600) if self.monthly_time else 1

        return int(round(min(dist_progress, time_progress) * 100, 0))

    def yearly_progress(self, distance=0, time=0):
        """Returns yearly progress percentage.
        Arguments:
            distance: completed distance
            time: time spent
        """

        if distance is None:
            distance = 0
        if time is None:
            time = 0

        dist_progress = distance / float(self.yearly_distance * 1000) if self.yearly_distance else 1
        time_progress = time / float(self.yearly_time * 3600) if self.yearly_time else 1

        return int(round(min(dist_progress, time_progress) * 100, 0))

    def has_weekly(self):
        """User has an active weekly goal."""

        return self.weekly_time or self.weekly_distance

    def has_monthly(self):
        """User has an active monthly goal."""

        return self.monthly_time or self.monthly_distance

    def has_yearly(self):
        """User has an active yearly goal."""

        return self.yearly_time or self.yearly_distance

    def has_any(self):
        """User has active goals."""

        return self.has_weekly() or self.has_monthly() or self.has_yearly()


@receiver(post_save, sender=User)
def create_related(sender, **kwargs):
    """Creates Goals object upon the creation of an user."""

    if kwargs.get('created', False):
        Goals.objects.get_or_create(user=kwargs.get('instance'))
