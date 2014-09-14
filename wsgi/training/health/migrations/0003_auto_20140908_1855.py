# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('health', '0002_auto_20140908_1810'),
    ]

    operations = [
        migrations.AlterField(
            model_name='athlete',
            name='height',
            field=models.IntegerField(null=True, verbose_name='height', blank=True),
        ),
        migrations.AlterField(
            model_name='athlete',
            name='lt_hr',
            field=models.IntegerField(null=True, verbose_name='lactate threshold heart rate', blank=True),
        ),
        migrations.AlterField(
            model_name='athlete',
            name='lt_power',
            field=models.IntegerField(null=True, verbose_name='functional threshold power', blank=True),
        ),
        migrations.AlterField(
            model_name='athlete',
            name='max_hr',
            field=models.IntegerField(null=True, verbose_name='maximum heart rate', blank=True),
        ),
        migrations.AlterField(
            model_name='athlete',
            name='max_power',
            field=models.IntegerField(null=True, verbose_name='maximum power', blank=True),
        ),
        migrations.AlterField(
            model_name='athlete',
            name='resting_hr',
            field=models.IntegerField(null=True, verbose_name='resting hear rate', blank=True),
        ),
    ]
