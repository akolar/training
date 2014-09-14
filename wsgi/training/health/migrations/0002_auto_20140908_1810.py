# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('health', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='athlete',
            name='weight',
        ),
        migrations.AlterField(
            model_name='athlete',
            name='lt_power',
            field=models.IntegerField(verbose_name='functional threshold power'),
        ),
    ]
