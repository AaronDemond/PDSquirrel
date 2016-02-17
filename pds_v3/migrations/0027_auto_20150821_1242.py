# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('pds_v3', '0026_auto_20150821_1153'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pdsession',
            name='upload_date',
        ),
        migrations.AddField(
            model_name='pdsession',
            name='date_uploaded',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='notice',
            name='attachment',
            field=models.FileField(null=True, upload_to=b'attachments', blank=True),
        ),
        migrations.AlterField(
            model_name='purchase',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2015, 8, 21, 12, 42, 44, 966646)),
        ),
    ]
