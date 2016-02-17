# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('pds_v3', '0043_auto_20150901_1507'),
    ]

    operations = [
        migrations.AlterField(
            model_name='presenter',
            name='bio',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='purchase',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 2, 14, 56, 58, 94836)),
        ),
    ]
