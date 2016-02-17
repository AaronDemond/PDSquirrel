# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('pds_v3', '0011_auto_20150807_2124'),
    ]

    operations = [
        migrations.AddField(
            model_name='pdsession',
            name='edited',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='pdsession',
            name='last_edited',
            field=models.BooleanField(default=datetime.datetime(2015, 8, 18, 15, 1, 22, 739613, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='purchase',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2015, 8, 18, 15, 1, 3, 153665)),
        ),
    ]
