# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('pds_v3', '0053_auto_20151015_1257'),
    ]

    operations = [
        migrations.AddField(
            model_name='pdsession',
            name='pdaudio',
            field=models.ForeignKey(to='pds_v3.PdAudio', null=True),
        ),
        migrations.AlterField(
            model_name='purchase',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 21, 14, 53, 13, 213071)),
        ),
    ]
