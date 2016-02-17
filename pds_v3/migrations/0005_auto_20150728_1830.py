# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('pds_v3', '0004_auto_20150728_1759'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchase',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2015, 7, 28, 18, 30, 41, 45180)),
        ),
        migrations.AlterField(
            model_name='purchase',
            name='price',
            field=models.FloatField(),
        ),
    ]
