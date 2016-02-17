# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('pds_v3', '0019_auto_20150819_1503'),
    ]

    operations = [
        migrations.AddField(
            model_name='pdsessionedit',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2015, 8, 19, 15, 13, 15, 778560), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='purchase',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2015, 8, 19, 15, 13, 11, 4806)),
        ),
    ]
