# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('pds_v3', '0047_auto_20150908_1443'),
    ]

    operations = [
        migrations.AddField(
            model_name='notice',
            name='all_presenters',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='notice',
            name='is_read',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='purchase',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 9, 11, 49, 18, 780435)),
        ),
    ]
