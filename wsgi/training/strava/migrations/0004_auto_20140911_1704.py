# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('strava', '0003_remove_strava_active'),
    ]

    operations = [
        migrations.RenameField(
            model_name='strava',
            old_name='code',
            new_name='token',
        ),
    ]
