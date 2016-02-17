# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('pds_v3', '0014_auto_20150818_1507'),
    ]

    operations = [
        migrations.AddField(
            model_name='pdsession',
            name='presenter_approved',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='purchase',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2015, 8, 18, 16, 34, 48, 935293)),
        ),
    ]
