# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('pds_v3', '0046_auto_20150908_0946'),
    ]

    operations = [
        migrations.AddField(
            model_name='pdsession',
            name='release_date',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='purchase',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 8, 14, 43, 50, 240269)),
        ),
    ]
