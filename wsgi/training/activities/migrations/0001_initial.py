# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields
import djorm_pgarray.fields
import django.contrib.gis.db.models.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(verbose_name='timestamp')),
                ('sport', models.SmallIntegerField(default=-1, verbose_name='sport', choices=[(-1, 'Not set'), (0, 'Ride'), (1, 'Run'), (2, 'Swim'), (3, 'Hike'), (4, 'Walk'), (10, 'Alpine Ski'), (11, 'Backcountry Ski'), (12, 'Canoeing'), (13, 'Cross-country Skiing'), (14, 'Crossfit'), (15, 'Elliptical'), (16, 'Ice Skate'), (17, 'Inline Skate'), (18, 'Kayaking'), (19, 'Kitesurf'), (20, 'Nordic Ski'), (21, 'Rock Climbing'), (22, 'Roller Ski'), (23, 'Rowing'), (24, 'Snowboard'), (25, 'Snowshoe'), (26, 'Stair-Stepper'), (27, 'Stand Up Padding'), (28, 'Surfing'), (29, 'Weight Training'), (30, 'Workout'), (31, 'Yoga')])),
                ('description', models.CharField(max_length=100, verbose_name='Title', blank=True)),
                ('comments', models.TextField(verbose_name='comments', blank=True)),
                ('primary_objective', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='primary objective', choices=[(0, 'Not specified'), (1, 'Endurance'), (2, 'Muscular endurance'), (3, 'Anaerobic endurance'), (4, 'Technique'), (5, 'Power'), (6, 'Strength'), (7, 'Recovery')])),
                ('rating', models.PositiveSmallIntegerField(default=6, null=True, verbose_name='RPE')),
                ('elapsed', models.PositiveIntegerField(default=None, null=True, verbose_name='elapsed time')),
                ('moving', models.PositiveIntegerField(default=None, null=True, verbose_name='moving time')),
                ('total_distance', models.PositiveIntegerField(default=None, null=True, verbose_name='distance')),
                ('elevation_gain', models.PositiveIntegerField(default=None, null=True, verbose_name='elevation gain')),
                ('speed_avg', models.PositiveSmallIntegerField(default=None, null=True, verbose_name='average speed')),
                ('speed_max', models.PositiveSmallIntegerField(default=None, null=True, verbose_name='maximum speed')),
                ('hr_avg', models.PositiveSmallIntegerField(default=None, null=True, verbose_name='average heart rate')),
                ('hr_max', models.PositiveSmallIntegerField(default=None, null=True, verbose_name='maximum heart rate')),
                ('temperature_max', models.SmallIntegerField(default=None, null=True, verbose_name='maximum temperature')),
                ('temperature_avg', models.SmallIntegerField(default=None, null=True, verbose_name='average temperature')),
                ('zones_elevation', jsonfield.fields.JSONField(null=True, blank=True)),
                ('zones_speed', jsonfield.fields.JSONField(null=True, blank=True)),
                ('zones_hr', jsonfield.fields.JSONField(null=True, blank=True)),
                ('zones_grade', jsonfield.fields.JSONField(null=True, blank=True)),
                ('zones_cadence', jsonfield.fields.JSONField(null=True, blank=True)),
                ('zones_temperature', jsonfield.fields.JSONField(null=True, blank=True)),
                ('track', django.contrib.gis.db.models.fields.LineStringField(srid=4326, dim=3, null=True, blank=True)),
                ('time', djorm_pgarray.fields.SmallIntegerArrayField(dbtype='smallint')),
                ('distance', djorm_pgarray.fields.IntegerArrayField()),
                ('heart_rate', djorm_pgarray.fields.SmallIntegerArrayField(dbtype='smallint')),
                ('cadence', djorm_pgarray.fields.SmallIntegerArrayField(dbtype='smallint')),
                ('temperature', djorm_pgarray.fields.SmallIntegerArrayField(dbtype='smallint')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Equipment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=b'', max_length=50, verbose_name='name')),
                ('sport', models.SmallIntegerField(default=-1, verbose_name='sport', choices=[(-1, b'Other'), (0, b'Bike'), (1, b'Shoes')])),
                ('comment', models.CharField(default=b'', max_length=100, null=True, verbose_name='comment', blank=True)),
                ('user', models.ForeignKey(default=None, to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='activity',
            name='equipment',
            field=models.ForeignKey(default=None, blank=True, to='activities.Equipment', null=True, verbose_name='equipment'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='activity',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
