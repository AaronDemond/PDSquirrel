# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('pds_v3', '0021_auto_20150820_1053'),
    ]

    operations = [
        migrations.AddField(
            model_name='pdsessionedit',
            name='approved',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='purchase',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2015, 8, 20, 16, 27, 20, 910755)),
        ),
    ]
