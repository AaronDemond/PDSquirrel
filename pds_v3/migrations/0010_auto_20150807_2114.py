# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('pds_v3', '0009_auto_20150807_2107'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='completedsession',
            name='appuser',
        ),
        migrations.RemoveField(
            model_name='completedsession',
            name='session',
        ),
        migrations.AlterField(
            model_name='purchase',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2015, 8, 7, 21, 14, 45, 84214)),
        ),
        migrations.DeleteModel(
            name='CompletedSession',
        ),
    ]
