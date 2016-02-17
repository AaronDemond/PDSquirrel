# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('pds_v3', '0015_auto_20150818_1634'),
    ]

    operations = [
        migrations.AddField(
            model_name='pdsession',
            name='suspend_reason',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='pdsession',
            name='suspend_request',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='purchase',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2015, 8, 19, 14, 0, 31, 14795)),
        ),
    ]
