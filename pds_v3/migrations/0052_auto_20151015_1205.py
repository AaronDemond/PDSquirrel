# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('pds_v3', '0051_auto_20150924_1157'),
    ]

    operations = [
        migrations.AddField(
            model_name='pdaudio',
            name='appuser',
            field=models.ManyToManyField(to='pds_v3.AppUser', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='pdaudio',
            name='audio',
            field=models.FileField(null=True, upload_to=b'audio_files', blank=True),
        ),
        migrations.AlterField(
            model_name='purchase',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 15, 12, 5, 59, 456595)),
        ),
    ]
