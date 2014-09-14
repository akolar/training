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
            name='Details',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('gender', models.NullBooleanField(verbose_name='gender', choices=[(None, 'unknow'), (True, 'male'), (False, 'female')])),
                ('units', models.BooleanField(default=True, verbose_name='units', choices=[(True, 'Metric (kilometers, kilograms)'), (False, 'Imperial (miles, pounds)')])),
                ('avatar', models.ImageField(upload_to=b'avatars', verbose_name='avatar')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
