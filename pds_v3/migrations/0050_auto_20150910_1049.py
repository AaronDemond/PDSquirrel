# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('pds_v3', '0049_auto_20150909_1150'),
    ]

    operations = [
        migrations.AddField(
            model_name='presenter',
            name='image',
            field=models.FileField(null=True, upload_to=b'presenter_pics', blank=True),
        ),
        migrations.AlterField(
            model_name='purchase',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 10, 10, 49, 48, 93572)),
        ),
    ]
