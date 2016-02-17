# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('pds_v3', '0012_auto_20150818_1501'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pdsession',
            name='last_edited',
        ),
        migrations.AlterField(
            model_name='purchase',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2015, 8, 18, 15, 4, 49, 674715)),
        ),
    ]
