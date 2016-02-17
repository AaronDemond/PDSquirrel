# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('pds_v3', '0022_auto_20150820_1627'),
    ]

    operations = [
        migrations.AddField(
            model_name='pdsession',
            name='total_sales',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='purchase',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2015, 8, 21, 11, 36, 34, 411977)),
        ),
    ]
