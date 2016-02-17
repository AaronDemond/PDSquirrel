# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('pds_v3', '0024_auto_20150821_1139'),
    ]

    operations = [
        migrations.AddField(
            model_name='pdsession',
            name='total_credits',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='purchase',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2015, 8, 21, 11, 45, 6, 439524)),
        ),
    ]
