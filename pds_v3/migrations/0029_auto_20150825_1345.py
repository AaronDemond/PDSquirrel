# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('pds_v3', '0028_auto_20150821_1243'),
    ]

    operations = [
        migrations.AddField(
            model_name='pdsessionedit',
            name='audio_file',
            field=models.FileField(null=True, upload_to=b'audio_files', blank=True),
        ),
        migrations.AddField(
            model_name='pdsessionedit',
            name='subjects',
            field=models.ManyToManyField(to='pds_v3.Subject', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='purchase',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2015, 8, 25, 13, 45, 53, 717431)),
        ),
    ]
