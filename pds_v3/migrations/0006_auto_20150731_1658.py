# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('pds_v3', '0005_auto_20150728_1830'),
    ]

    operations = [
        migrations.AddField(
            model_name='appuser',
            name='stripe_id',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='purchase',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2015, 7, 31, 16, 58, 55, 43949)),
        ),
    ]
