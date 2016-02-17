# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('pds_v3', '0006_auto_20150731_1658'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchase',
            name='credit_used',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='purchase',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2015, 8, 7, 20, 23, 11, 974929)),
        ),
    ]
