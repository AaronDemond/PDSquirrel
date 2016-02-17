# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('pds_v3', '0055_auto_20151031_1500'),
    ]

    operations = [
        migrations.AddField(
            model_name='pdaudio',
            name='hidden',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='purchase',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 24, 17, 24, 16, 278899)),
        ),
    ]
