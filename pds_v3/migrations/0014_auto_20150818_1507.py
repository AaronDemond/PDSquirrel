# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('pds_v3', '0013_auto_20150818_1504'),
    ]

    operations = [
        migrations.AddField(
            model_name='pdsession',
            name='last_edited',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='purchase',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2015, 8, 18, 15, 7, 4, 140933)),
        ),
    ]
