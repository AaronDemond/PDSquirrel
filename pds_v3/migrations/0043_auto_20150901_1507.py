# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('pds_v3', '0042_auto_20150901_1455'),
    ]

    operations = [
        migrations.AddField(
            model_name='pdsession',
            name='total_takes',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='purchase',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 1, 15, 7, 22, 462956)),
        ),
    ]
