# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('strava', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='strava',
            name='active',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='strava',
            name='last_access',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
