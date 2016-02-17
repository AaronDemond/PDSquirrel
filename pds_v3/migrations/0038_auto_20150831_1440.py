# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('pds_v3', '0037_auto_20150831_1247'),
    ]

    operations = [
        migrations.AddField(
            model_name='pdsessionedit',
            name='presenter_approved',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='purchase',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2015, 8, 31, 14, 40, 51, 69297)),
        ),
    ]
