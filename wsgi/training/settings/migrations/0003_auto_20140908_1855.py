# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('settings', '0002_auto_20140908_1810'),
    ]

    operations = [
        migrations.AlterField(
            model_name='details',
            name='avatar',
            field=models.ImageField(upload_to=b'avatars', null=True, verbose_name='avatar'),
        ),
        migrations.AlterField(
            model_name='details',
            name='gender',
            field=models.NullBooleanField(default=None, verbose_name='gender', choices=[(None, 'unknown'), (True, 'male'), (False, 'female')]),
        ),
    ]
