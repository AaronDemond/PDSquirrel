# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('pds_v3', '0020_auto_20150819_1513'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pdsession',
            old_name='release_date',
            new_name='upload_date',
        ),
        migrations.AlterField(
            model_name='purchase',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2015, 8, 20, 10, 53, 49, 875266)),
        ),
    ]
