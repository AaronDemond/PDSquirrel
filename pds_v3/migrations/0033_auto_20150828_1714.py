# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('pds_v3', '0032_auto_20150828_1656'),
    ]

    operations = [
        migrations.AddField(
            model_name='pdattachment',
            name='name',
            field=models.CharField(max_length=b'100', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='purchase',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2015, 8, 28, 17, 14, 3, 938793)),
        ),
    ]
