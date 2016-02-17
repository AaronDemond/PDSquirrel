# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('pds_v3', '0034_auto_20150828_1756'),
    ]

    operations = [
        migrations.AddField(
            model_name='appuser',
            name='date_premium',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='pdsession',
            name='price',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='purchase',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2015, 8, 31, 10, 59, 2, 530104)),
        ),
    ]
