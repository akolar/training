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
                ('resting_hr', models.IntegerField(null=True, verbose_name='resting hear rate', blank=True)),
                ('max_hr', models.IntegerField(null=True, verbose_name='maximum heart rate', blank=True)),
                ('lt_hr', models.IntegerField(null=True, verbose_name='lactate threshold heart rate', blank=True)),
                ('max_power', models.IntegerField(null=True, verbose_name='maximum power', blank=True)),
                ('lt_power', models.IntegerField(null=True, verbose_name='functional threshold power', blank=True)),
                ('height', models.IntegerField(null=True, verbose_name='height', blank=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
