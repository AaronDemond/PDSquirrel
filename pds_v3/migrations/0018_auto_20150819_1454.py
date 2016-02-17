# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('pds_v3', '0017_auto_20150819_1454'),
    ]

    operations = [
        migrations.AddField(
            model_name='pdsession',
            name='edits',
            field=models.ManyToManyField(to='pds_v3.PdSessionEdit', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='purchase',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2015, 8, 19, 14, 54, 57, 971399)),
        ),
    ]
