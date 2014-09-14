# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('settings', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='details',
            name='gender',
            field=models.NullBooleanField(verbose_name='gender', choices=[(None, 'unknown'), (True, 'male'), (False, 'female')]),
        ),
    ]
