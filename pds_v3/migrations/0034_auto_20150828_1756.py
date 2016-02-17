# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('pds_v3', '0033_auto_20150828_1714'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pdsession',
            name='price',
            field=models.FloatField(default=b'9.99', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='purchase',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2015, 8, 28, 17, 56, 44, 160994)),
        ),
    ]
