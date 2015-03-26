from django.db import models
from django.contrib.auth.models import User

from djorm_pgarray.fields import IntegerArrayField


class Strava(models.Model):
    user = models.OneToOneField(User)

    token = models.CharField(max_length=40, null=True)
    granted = models.DateTimeField(auto_now_add=True)

    last_access = models.DateTimeField(auto_now=True)
    fetched = IntegerArrayField(default=[])
