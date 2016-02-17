# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('pds_v3', '0054_auto_20151021_1453'),
    ]

    operations = [
        migrations.AddField(
            model_name='pdaudio',
            name='used',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='purchase',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 31, 15, 0, 43, 574303)),
        ),
    ]
