# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('pds_v3', '0052_auto_20151015_1205'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pdaudio',
            name='appuser',
        ),
        migrations.AddField(
            model_name='pdaudio',
            name='appuser',
            field=models.ForeignKey(blank=True, to='pds_v3.AppUser', null=True),
        ),
        migrations.AlterField(
            model_name='purchase',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 15, 12, 57, 49, 438548)),
        ),
    ]
