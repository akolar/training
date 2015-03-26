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
            name='Goals',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('weekly_distance', models.IntegerField(default=0, verbose_name='weekly goal (distance)')),
                ('weekly_time', models.IntegerField(default=0, verbose_name='weekly goal (time)')),
                ('monthly_distance', models.IntegerField(default=0, verbose_name='monthly goal (distance)')),
                ('monthly_time', models.IntegerField(default=0, verbose_name='monthly goal (time)')),
                ('yearly_distance', models.IntegerField(default=0, verbose_name='yearly goal (distance)')),
                ('yearly_time', models.IntegerField(default=0, verbose_name='yearly goal (time)')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
