# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('pds_v3', '0048_auto_20150909_1149'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notice',
            name='all_presenters',
        ),
        migrations.AlterField(
            model_name='purchase',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 9, 11, 50, 39, 510799)),
        ),
    ]
