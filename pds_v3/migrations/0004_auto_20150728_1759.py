# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('pds_v3', '0003_auto_20150728_1756'),
    ]

    operations = [
        migrations.AddField(
            model_name='appuser',
            name='is_premium',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='appuser',
            name='remaining_pd',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='purchase',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2015, 7, 28, 17, 59, 21, 41937)),
        ),
    ]
