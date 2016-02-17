# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('pds_v3', '0027_auto_20150821_1242'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pdsession',
            old_name='date_uploaded',
            new_name='upload_date',
        ),
        migrations.AlterField(
            model_name='purchase',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2015, 8, 21, 12, 43, 31, 743367)),
        ),
    ]
