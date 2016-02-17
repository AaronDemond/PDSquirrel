# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('pds_v3', '0036_auto_20150831_1110'),
    ]

    operations = [
        migrations.AddField(
            model_name='pdsession',
            name='locked',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='purchase',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2015, 8, 31, 12, 47, 16, 694363)),
        ),
    ]
