# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Athlete',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('resting_hr', models.IntegerField(verbose_name='resting hear rate')),
                ('max_hr', models.IntegerField(verbose_name='maximum heart rate')),
                ('lt_hr', models.IntegerField(verbose_name='lactate threshold heart rate')),
                ('max_power', models.IntegerField(verbose_name='maximum power')),
                ('lt_power', models.IntegerField(verbose_name='lactate threshold power')),
                ('weight', models.FloatField(verbose_name='weight')),
                ('height', models.IntegerField(verbose_name='height')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
